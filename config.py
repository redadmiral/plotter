PLOT_TYPES = ["tikz", "matplotlib"]

GERBIL_BASE_URL = "http://141.13.94.164:1234/gerbil/"
FDIS_BASE_URL = "https://www.vm14.frontend.kinf.wiai.uni-bamberg.de"
FDIS_GERBIL_ENDPOINT = "gerbil"

GRAPH = [
              'dbpedia_500_4_cbow_200',
              'dbpedia_500_4_sg_100',
              'wikidata_pbg',
              'dbpedia_500_4_sg_200'
]

EXPERIMENTS = {
"Graph",
"Wsim",
"Wrank",
"Exprank",
"Expsim",
"Lowlatency",
}

data = {
"type" : "A2KB",
"matching" : "WEAK_ANNOTATION_MATCH",
"annotator" : ["NIFWS_tfdis(https://www.vm14.frontend.kinf.wiai.uni-bamberg.de/gerbil)"],
"dataset" : ["NIFDS_news100(News-100.ttl)"]
}

## TEST ALOE

ALOE_ARTICLES = "articles.csv"