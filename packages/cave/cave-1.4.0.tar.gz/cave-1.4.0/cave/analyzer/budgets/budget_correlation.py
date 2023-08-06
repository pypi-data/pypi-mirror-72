import warnings
from typing import List

from bokeh.embed import components
from bokeh.io import output_notebook
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Range1d
from bokeh.models.widgets import DataTable, TableColumn, Select
from bokeh.plotting import show, figure
from pandas import DataFrame
from scipy.stats import spearmanr

from cave.analyzer.base_analyzer import BaseAnalyzer
from cave.utils.hpbandster_helpers import format_budgets


class BudgetCorrelation(BaseAnalyzer):
    """
    Use spearman correlation to get a correlation-value and a p-value for every pairwise combination of budgets.
    First value is the correlation, second is the p-value (the p-value roughly estimates the likelihood to obtain
    this correlation coefficient with uncorrelated datasets).
    This can be used to estimate how well a budget approximates the function to be optimized.
    """

    def __init__(self,
                 runscontainer):
        """
        Parameters
        ----------
        runscontainer: RunsContainer
            contains all important information about the configurator runs
        """
        super().__init__(runscontainer)

        self.runs = self.runscontainer.get_aggregated(keep_budgets=True, keep_folders=False)
        self.budget_names = list(format_budgets(self.runscontainer.get_budgets(), allow_whitespace=True).values())
        self.logger.debug("Budget names: %s", str(self.budget_names))

        # To be set
        self.dataframe = None

    def get_name(self):
        return "Budget Correlation"

    def _get_table(self, runs):
        table = []
        for b1 in runs:
            table.append([])
            for b2 in runs:
                configs = set(b1.combined_runhistory.get_all_configs()).intersection(
                                set(b2.combined_runhistory.get_all_configs()))
                if len(configs) < 1:
                    table[-1].append("N/A")
                    continue
                costs = list(zip(*[(b1.combined_runhistory.get_cost(c),
                                    b2.combined_runhistory.get_cost(c)) for c in configs]))
                rho, p = spearmanr(costs[0], costs[1])
                # Differentiate to generate upper diagonal
                if runs.index(b2) < runs.index(b1):
                    table[-1].append("")
                else:
                    table[-1].append("{:.2f} ({} samples)".format(rho, len(costs[0])))

        return DataFrame(data=table, columns=self.budget_names, index=self.budget_names)

    def plot(self):
        """Create table and plot that reacts to selection of cells by updating the plotted data to visualize
        correlation."""
        return self._plot(self.runs)

    def _plot(self, runs):
        """
        Create table and plot that reacts to selection of cells by updating the plotted data to visualize correlation.

        Parameters
        ----------
        runs: List[ConfiguratorRun]
            list with runs (budgets) to be compared
        """
        df = self._get_table(runs)
        # Create CDS from pandas dataframe
        budget_names = list(df.columns.values)
        data = dict(df[budget_names])
        data["Budget"] = df.index.tolist()
        table_source = ColumnDataSource(data)
        # Create bokeh-datatable
        columns = [TableColumn(field='Budget', title="Budget", sortable=False, width=20)] + [
                   TableColumn(field=header, title=header, default_sort='descending', width=10)
                   for header in budget_names
                  ]
        bokeh_table = DataTable(source=table_source, columns=columns, index_position=None, sortable=False,
                                height=20 + 30 * len(data["Budget"]))

        # Create CDS for scatter-plot
        all_configs = set([a for b in [run.original_runhistory.get_all_configs() for run in runs] for a in b])
        data = {self.budget_names[idx]: [run.original_runhistory.get_cost(c) if c in  # TODO
                                         run.original_runhistory.get_all_configs() else
                                         None for c in all_configs] for idx, run in enumerate(runs)}
        data['x'] = []
        data['y'] = []
        # Default scatter should be lowest vs highest:
        for x, y in zip(data[budget_names[0]], data[budget_names[-1]]):
            if x is not None and y is not None:
                data['x'].append(x)
                data['y'].append(y)

        with warnings.catch_warnings(record=True) as list_of_warnings:
            # Catch unmatching column lengths warning
            warnings.simplefilter('always')
            scatter_source = ColumnDataSource(data=data)
            for w in list_of_warnings:
                self.logger.debug("During budget correlation a %s was raised: %s", str(w.category), w.message)

        # Create figure and dynamically updating plot (linked with table)
        min_val = min([min([v for v in val if v]) for val in data.values() if len(val) > 0])
        max_val = max([max([v for v in val if v]) for val in data.values() if len(val) > 0])
        padding = (max_val - min_val) / 10  # Small padding to border (fraction of total intervall)
        min_val -= padding
        max_val += padding
        p = figure(plot_width=400, plot_height=400,
                   match_aspect=True,
                   y_range=Range1d(start=min_val, end=max_val, bounds=(min_val, max_val)),
                   x_range=Range1d(start=min_val, end=max_val, bounds=(min_val, max_val)),
                   x_axis_label=budget_names[0], y_axis_label=budget_names[-1])
        p.circle(x='x', y='y',
                 # x=jitter('x', 0.1), y=jitter('y', 0.1),
                 source=scatter_source, size=5, color="navy", alpha=0.5)

        code_budgets = 'var budgets = ' + str(budget_names) + '; console.log(budgets);'

        code_try = 'try {'
        code_get_selected_cell = """
            // This first part only extracts selected row and column!
            var grid = document.getElementsByClassName('grid-canvas')[0].children;
            var row = '';
            var col = '';
            for (var i=0,max=grid.length;i<max;i++){
                if (grid[i].outerHTML.includes('active')){
                    row=i;
                    for (var j=0,jmax=grid[i].children.length;j<jmax;j++){
                        if(grid[i].children[j].outerHTML.includes('active')){col=j}
                    }
                }
            }
            col = col - 1;
            console.log('row', row, budgets[row]);
            console.log('col', col, budgets[col]);
            table_source.selected.indices = [];  // Reset, so gets triggered again when clicked again
        """

        code_selected = """
        row = budgets.indexOf(select_x.value);
        col = budgets.indexOf(select_y.value);
        """

        code_update_selection_values = """
        select_x.value = budgets[row];
        select_y.value = budgets[col];
        """

        code_update_plot = """
            // This is the actual updating of the plot
            if (row =>  0 && col > 0) {
              // Copy relevant arrays
              var new_x = scatter_source.data[budgets[row]].slice();
              var new_y = scatter_source.data[budgets[col]].slice();
              // Remove all pairs where one value is null
              while ((next_null = new_x.indexOf(null)) > -1) {
                new_x.splice(next_null, 1);
                new_y.splice(next_null, 1);
              }
              while ((next_null = new_y.indexOf(null)) > -1) {
                new_x.splice(next_null, 1);
                new_y.splice(next_null, 1);
              }
              // Assign new data to the plotted columns
              scatter_source.data['x'] = new_x;
              scatter_source.data['y'] = new_y;
              scatter_source.change.emit();
              // Update axis-labels
              xaxis.attributes.axis_label = budgets[row];
              yaxis.attributes.axis_label = budgets[col];
              // Update ranges
              var min = Math.min(...[Math.min(...new_x), Math.min(...new_y)])
                  max = Math.max(...[Math.max(...new_x), Math.max(...new_y)]);
              var padding = (max - min) / 10;
              console.log(min, max, padding);
              xr.start = min - padding;
              yr.start = min - padding;
              xr.end = max + padding;
              yr.end = max + padding;
            }
        """

        code_catch = """
        } catch(err) {
            console.log(err.message);
        }
        """

        code_selected = code_budgets + code_try + code_selected + code_update_plot + code_catch
        select_x = Select(title="X-axis:", value=budget_names[0],  options=budget_names)
        select_y = Select(title="Y-axis:", value=budget_names[-1], options=budget_names)
        callback_select = CustomJS(args=dict(scatter_source=scatter_source,
                                             select_x=select_x, select_y=select_y,
                                             xaxis=p.xaxis[0], yaxis=p.yaxis[0],
                                             xr=p.x_range, yr=p.y_range,
                                             ), code=code_selected)
        select_x.js_on_change('value', callback_select)
        select_y.js_on_change('value', callback_select)

        code_table_cell = code_budgets + code_try + code_get_selected_cell + code_update_selection_values
        code_table_cell += code_update_plot + code_catch
        callback_table_cell = CustomJS(args=dict(table_source=table_source,
                                                 scatter_source=scatter_source,
                                                 select_x=select_x, select_y=select_y,
                                                 xaxis=p.xaxis[0], yaxis=p.yaxis[0],
                                                 xr=p.x_range, yr=p.y_range,
                                                 ), code=code_table_cell)
        table_source.selected.js_on_change('indices', callback_table_cell)

        layout = column(bokeh_table, row(p, column(select_x, select_y)))
        return layout

    def get_html(self, d=None, tooltip=None):
        script, div = components(self.plot())
        if d is not None:
            d["Budget Correlation"] = {
                "bokeh": (script, div),
                "tooltip": self.__doc__,
            }
        return script, div

    def get_jupyter(self):
        output_notebook()
        show(self.plot())
