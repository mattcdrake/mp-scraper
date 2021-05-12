from flask import Flask, request, Response
from bs4 import BeautifulSoup
from urllib import request as urlreq
from pandas import pandas as pd
import json

app = Flask(__name__)


@app.route("/", methods=['POST'])
def scrape_wiki():
    """
    Parses the HTML at the requested URL for <table> elements. It then calls a helper function to convert that HTML into
    a dictionary of dictionaries. That dictionary is converted to JSON and sent back as in the HTTP response.

    :return: JSON dump of the tables on the given Wiki page.
    """
    req_json = request.get_json()
    url = req_json.get("url", "")
    if url == "":
        return Response("You must supply a valid wikipedia URL", mimetype="text/plain", status=400)

    skiprows = int(req_json.get("skiprows", 0))
    try:
        page = urlreq.urlopen(url)
    except:
        return Response("Unable to access the supplied URL", mimetype="text/plain", status=400)

    try:
        page_soup = BeautifulSoup(page, "html.parser")
    except:
        return Response("Supplied URL does not consist of valid HTML.", mimetype="text/plain", status=400)

    tables = page_soup.find_all("table", class_="wikitable")
    tables_dict = convert_wiki_tables(tables, skiprows)
    return Response(json.dumps(tables_dict), mimetype='application/json', status="200")


def convert_wiki_tables(tables, skiprows: int):
    """
    Converts HTML tables (parsed by BeautifulSoup) into a dictionary of dictionaries. Uses dataframes for intermediate
    data representation. This is because pandas is good at handling tables where row/colspan > 1. These tables are not
    NxM since some cells in the HTML will account for more than one cell.

    :param tables: A list of <table> strings, pparsed by BeautifulSoup
    :param skiprows: Number of rows to skip for each table
    :return: Dictionary of dictionaries
    """
    dict_tables = {"bad_tables": 0}

    for i, table in enumerate(tables):
        try:
            table_df = pd.read_html(str(table), flavor="bs4", skiprows=skiprows)[0]
            dict_tables[i] = table_df.where((pd.notnull(table_df)), None).to_dict("records")
        except:
            dict_tables["bad_tables"] = dict_tables.get("bad_tables", 0) + 1

    return dict_tables


if __name__ == '__main__':
    app.run()
