from experiment import Experiment
import pandas as pd
import matplotlib.pyplot as plt
import tikzplotlib
import config

tests = ["A2KB", "ER", "D2KB"]

""" All values:
[           'Annotator',              'Dataset',           'Unnamed: 2',
       'Micro F1 score',      'Micro Precision',         'Micro Recall',
       'Macro F1 score',      'Macro Precision',         'Macro Recall',
  'InKB Macro F1 score', 'InKB Macro Precision',    'InKB Macro Recall',
  'InKB Micro F1 score', 'InKB Micro Precision',    'InKB Micro Recall',
    'EE Macro F1 score',   'EE Macro Precision',      'EE Macro Recall',
    'EE Micro F1 score',   'EE Micro Precision',      'EE Micro Recall',
       'avg millis/doc', 'confidence threshold',          'Error Count',
            'Timestamp',       'GERBIL version']
"""

columns = ['Annotator',              'Dataset',           'Unnamed: 2',
       'Macro F1 score',      'Macro Precision',         'Macro Recall']
wanted_plots = {
    "news100 (uploaded)": ["A2KB"]
}

experiment_ids = pd.read_csv("dispatched_experiments.csv")
plots = list()
for id in experiment_ids["id"]:
    url = config.GERBIL_BASE_URL + "experiment?id=" + str(id)
    experiment = Experiment(URL=url, measures=columns)
    plots.append(experiment.create_plots(wanted_plots))

plt.show()