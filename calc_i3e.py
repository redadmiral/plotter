import pandas as pd

triples = pd.read_csv("SollTripel.csv", sep=",", skip_blank_lines=True, skipinitialspace=True)
triples.columns = ["triple", "found"]
triples = triples["#" not in triples.triple]

print(triples)