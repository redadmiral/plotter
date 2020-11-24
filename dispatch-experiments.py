import config
import pandas as pd
import requests
from typing import List, Dict
import logging
import time

logging.basicConfig(filename="plotter.log", level=logging.INFO)

def dispatch_tests(experiments: List[str]) -> None:
    experiment: str
    for experiment in experiments:
        experiment_data: pd.DataFrame = pd.read_csv("".join(["experiments/gerbil_", experiment, ".csv"]), header=0)
        id: int = send_experiment_to_gerbil(experiment, experiment_data)
        print("http://141.13.94.164:1234/gerbil/experiment?id=" + id)
        logging.info(time.ctime() + ": Experiment of type " + experiment + " successufully dispatched. ID " + str(id) + " returned.")



def send_experiment_to_gerbil(experiment: str, experiment_data: pd.DataFrame) -> str:
    fdis_urls: Dict[str, str] = create_annotator_urls(experiment_data, experiment)
    query: str = create_query(fdis_urls)
    logging.info(time.ctime() + ": " + query)
    response = requests.get(query)
    try:
        return str(int(response.content))
    except ValueError as e:
        print(response.content)
        raise requests.exceptions.ConnectionError()

def create_annotator_urls(experiment_data: pd.DataFrame, experiment: str) -> Dict[str, str]:
    annotators: Dict[str, str] = dict()
    parameters: List[str] = list()
    parameters = experiment_data.apply(create_parameter, axis=1)
    for i in range(len(parameters)):
        if type(experiment_data[experiment][i]) is str:
            changed_value = experiment_data[experiment][i].replace("_", "-")
        else:
            changed_value = str(experiment_data[experiment][i])

        annotators[str("_".join(["fdis", experiment, changed_value]))] = config.FDIS_BASE_URL + "/gerbil?" + parameters[i]
    return annotators

def create_parameter(row: pd.Series) -> str:
    result: List[str] = list()
    for colname, value in row.items():
        result.append("=".join([colname, str(value)]))
    return "%26".join(result)

def create_query(fdis_urls: Dict[str, str]) -> str:
    urls: List[str] = list()
    for experiment, url in fdis_urls.items():
        entry: str = "_".join(["NIFWS", experiment]) + "(" + url + ")"
        urls.append(entry)

    data =   {
    "type" : "A2KB",
    "matching" : "WEAK_ANNOTATION_MATCH",
    "annotator" : urls,
    "dataset" : ["NIFDS_news100(News-100.ttl)"]
    }

    query = str(config.GERBIL_BASE_URL + "execute?experimentData=" + str(data)).replace("'", '"')
    return query


if __name__ == '__main__':
    dispatch_tests(["wsim"])
