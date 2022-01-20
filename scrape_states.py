import pandas as pd

def scrape():
    url = "https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=53971"
    html = pd.read_html(url)

    states_table = html[0]
    states = []
    states = states_table["Alpha code"]

    return states
