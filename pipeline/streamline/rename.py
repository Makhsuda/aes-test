import pandas as pd

"""Rename.py

Renames the CSV headers to their correct taxonomies used in other scripts.
"""


# Define Taxonomy headers for data
# idx, company, city, tax1, tax2, tax3, website, lat, lng
# company = ["organization name"]
# city = ["city"]
# tax1 = ["sector - 1", "sector 1"]
# tax2 = ["sector - 2", "sector 2"]
# tax3 = ["sector - 3", "sector 3"]
# website = ["website"]
# lat = ["latitude (dd)", "latitude", "lat"]
# lng = ["longitude (dd)", "longitude", "long", "lng"]

# TODO: Instead of Dictionary, use REGEX
company = {
    "organization name" : "company",
    "company" : "company"
}
city = {
    "city" : "city"
}
tax1 = {
    "sector - 1" : "tax1",
    "sector 1" : "tax1",
}
tax2 = {
    "sector - 2" : "tax1",
    "sector 2" : "tax1",
}
tax3 = {
    "sector - 3" : "tax1",
    "sector 3" : "tax1",
}
website = {
    "website" : "website"
}
lat = {
    "latitude (dd)" : "lat",
    "latitude" : "lat",
    "lat" : "lat",
    "lati" : "lati"
}
lng = {
    "longitude (dd)" : "lng",
    "longitude" : "lng",
    "long" : "lng",
    "lng" : "lng"
}
columns = company | city | tax1 | tax2 | tax3 | website | lat | lng

# Retrieve Pandas Dataframe and headers
# TODO: Parametrize this in a command line argument
df = pd.read_csv("data/test.csv", nrows=1)
headers = df.columns
print(len(df.columns))

def change_names(headers):
    # TODO: Add doc and split into separate function?
    global column_ptrs
    new_column_names = {}
    for col in headers:
        try:
            new_column_names[col] = columns[col.lower()]
        except:
            new_column_names[col] = col
    return new_column_names.copy()

df.rename(columns=change_names(headers), inplace=True)

df.to_csv("data/test_output.csv")

# Adds 'idx' column to csv
# import pandas as pd
# import sys

# input_file = sys.argv[1]
# df = pd.read_csv(input_file)
# df.index.name = 'idx'
# df.round(6).to_csv(input_file)