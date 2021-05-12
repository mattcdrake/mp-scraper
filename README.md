# Wiki Tables to JSON Scraper

## Request

Make a HTTP GET request to `<api-url>/`. The request body should be JSON.

This API accepts the following parameters:

**url**: The Wikipedia page to parse
**skiprows**: (Defaults to 0) The number of rows to skip. This is usually 0 but
some pages have tables with useless rows at the top.

### Example Request

```json
{
    "url":"https://en.wikipedia.org/wiki/List_of_2021_albums",
    "skiprows": 1
}
```

## Response

The API will send a JSON response where each table is an array of objects, starting
with index 0. So, the first table will be the array at index 0. The second, 1,
and so on.

Within a table, each row is represented as an object. If the table has column
titles, that will be the first object in the array.

`bad_tables` will inform the caller of the number of tables that have malformed 
`<table>` elements and cannot be parsed by the API. Due to the nature of Wikipedia,
this is somewhat common.

### Example Response

```json
{
    "bad_tables": 0,
    "0": [
        {
            "0": "Release date",
            "1": "Artist",
            "2": "Album",
            "3": "Genre",
            "4": "Label",
            "5": "Ref.",
            "6": null,
            "7": null,
            "8": null
        },
        {
            "0": "January 1",
            "1": "Agallah Don Bishop",
            "2": "2021",
            "3": null,
            "4": null,
            "5": "[1]",
            "6": null,
            "7": null,
            "8": null
        },
        {
            "0": "January 1",
            "1": "Anavitória",
            "2": "Cor",
            "3": "Folk-pop",
            "4": "Anavitória Artes",
            "5": "[2]",
            "6": null,
            "7": null,
            "8": null
        }
    ],
    "1": [
        {
            "0": "Release date",
            "1": "Artist",
            "2": "Album",
            "3": "Genre",
            "4": "Label",
            "5": "Ref.",
            "6": null,
            "7": null,
            "8": null
        },
        {
            "0": "February2",
            "1": "Capicua",
            "2": "Encore",
            "3": null,
            "4": null,
            "5": "[193]",
            "6": null,
            "7": null,
            "8": null
        },
        {
            "0": "February2",
            "1": "CIX",
            "2": "Hello Chapter Ø: Hello, Strange Dream",
            "3": null,
            "4": "C9",
            "5": "[194]",
            "6": null,
            "7": null,
            "8": null
        }
    ]
}
```
