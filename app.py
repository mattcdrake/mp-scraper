from flask import Flask, request, Response
from bs4 import BeautifulSoup
from urllib import request as urlreq
from pandas import pandas as pd
import json

app = Flask(__name__)
url = "https://en.wikipedia.org/wiki/List_of_2021_albums"


@app.route("/")
def scrape_wiki():
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
    tables_dict = print_wiki(tables, skiprows)
    return Response(json.dumps(tables_dict), mimetype='application/json', status="200")


def print_wiki(tables, skiprows: int):
    dict_tables = {"bad_tables": 0}

    for i, table in enumerate(tables):
        try:
            table_df = pd.read_html(str(table), flavor="bs4", skiprows=skiprows)[0]
            dict_tables[i] = table_df.where((pd.notnull(table_df)), None).to_dict()
        except:
            dict_tables["bad_tables"] = dict_tables.get("bad_tables", 0) + 1

    return dict_tables


if __name__ == '__main__':
    app.run()
