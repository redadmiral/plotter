import pandas as pd
from typing import List, Dict, Any
import config
import matplotlib.pyplot as plt

class Experiment:
    def __init__(self, URL: str, measures: List[str]):
        self.measures: List[str] = measures
        self.table: pd.Dataframe = self.download_table(URL)
        self.datasets: List[str] = pd.unique(self.table["Dataset"])
        self.tests: List[str] = pd.unique(self.table["Unnamed: 2"])
        self.dataframes: Dict[str, Dict[str, pd.DataFrame]] = self.create_sub_dataframes()

    def download_table(self, URL: str) -> pd.DataFrame:
        table = pd.read_html(URL)[0][self.measures]
        table["Unnamed: 2"] = table["Unnamed: 2"].fillna("A2KB")
        table["Unnamed: 2"] = table["Unnamed: 2"].replace("Entity Recognition", "ER")
        return table

    def get_datasets(self) -> List[str]:
        return self.datasets

    def create_sub_dataframes(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Splits the large table in smaller tables, representing one test for one dataset each.
        :return:
        """

        dataframes: Dict[str, Dict[str, pd.DataFrame]] = dict()
        for dataset in self.datasets:
            dataset_table: pd.DataFrame = self.table[self.table["Dataset"]==dataset]
            test_tables = dict()
            for test in self.tests:
                test_tables[test] = dataset_table[dataset_table["Unnamed: 2"]==test]
            dataframes[dataset] = test_tables

        return dataframes

    def get_experiment_values(self, parameter: str):
        values = parameter.split("_")[-1].split(" ")[0]
        try:
            return float(values)
        except ValueError:
            return values

    def get_experiment_type(self, parameter: str):
        return parameter.split("_")[-2:-1]

    def create_plots(self, datasets: Dict[str, List[str]], plottype="tikz"):
        """
        Returns a list of plots, as specified in the datasets parameter. datasets takes a dict, with names of the
        datasets as keys and all test for which plots shall be produced ("A2KB", "ER", "D2KB").
        :return: List of plots in the specified format.
        """

        if plottype not in config.PLOT_TYPES:
            raise ValueError(plottype + " is not a valid plot type. Must be" + ", ".join(config.PLOT_TYPES + ".\n"))

        plots: List[Any] = list()

        for dataset, tests in datasets.items():
            try:
                cur_dataset = self.dataframes[dataset]
            except KeyError:
                raise KeyError("No dataset named " + dataset + " found. Possible Datasets: " + str(self.get_datasets()))
            for test in tests:
                plotset = cur_dataset[test]
                experiment_type = list(plotset["Annotator"])[0].split("_")[-2:-1]
                plotset, x_label = self.parse_axis(plotset, "x")
                xticks = list(plotset["Annotator"].apply(self.get_experiment_values))
                plotset.index = xticks
                plot = plotset.plot(title=", ".join([dataset, test, experiment_type[0]]))
                if type(xticks[0]) == str:
                    plot.tick_params(axis="x", labelrotation=15)
                plot.set_xlabel(x_label)
                plot.set_ylim([0,1])
                plot.set_ylabel("from 1.")
                plots.append(plot)
        return plots

    def parse_axis(self, plotset: pd.DataFrame, axis = "x"):
        if axis == "x":
            label = list(plotset["Annotator"])[0]
            label = label.replace(" (NIF WS)", "")
            label = label.split("_")[-1]
            label = label[:-2]
            plotset["Annotator"].replace(label, "")
            return plotset, label
        else:
            raise NotImplementedError("Parsing of y or z axis is not implemented.")
