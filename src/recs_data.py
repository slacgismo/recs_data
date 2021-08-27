import os, sys
import openpyxl
import requests
import datetime
import pandas

baseurl = "https://www.eia.gov/consumption/residential/data/2015/hc/"
microdata_url = "https://www.eia.gov/consumption/residential/data/2015/csv/recs2015_public_v4.csv"
sources = {
    "2015" : {
        "hc1.1" : "Fuel use and end-uses by housing unit type",
    }
}

class HousingCharacteristics:
    table_structure = {
        "hc1.1" : {
            "units" : 1e6,
            "columns" : {
                "total" : "B",
                "unit-type" : {
                    "single-family-detached" : "C",
                    "single-family-attached" : "D",
                    "apartment-small" : "E",
                    "apartment-large" : "F",
                    "mobile-home" : "G",
                },
            },
            "rows" : {
                "total" : 6,
                "fuel-used" : {
                    "electricity" : 8,
                    "natural-gas" : 9,
                    "propane" : 10,
                    "wood" : 11,
                    "fuel-oil" : 12,
                },
                "electric-end-use" : {
                    "space-heating" : {
                        "total" : 14,
                        "main" : 15,
                        "secondary" : 16,
                        },
                    "air-conditioning" : 17,
                    "water-heating" : 18,
                    "cooking" : 19,
                },
                "natural-gas-end-use" : {
                    "space-heating" : {
                        "total" : 21,
                        "main" : 22,
                        "secondary" : 23,
                        },
                    "water-heating" : 24,
                    "cooking" : 25,
                    "outdoor-grilling" : 26,
                },
                "natural-gas-end-use" : {
                    "space-heating" : {
                        "total" : 28,
                        "main" : 29,
                        "secondary" : 30,
                        },
                    "water-heating" : 31,
                    "cooking" : 32,
                    "outdoor-grilling" : 33,
                },
                "wood-end-use" : {
                    "space-heating" : {
                        "total" : 35,
                        "main" : 36,
                        "secondary" : 37,
                        },
                    "water-heating" : 38,
                },
                "fuel-oil-end-use" : {
                    "space-heating" : {
                        "total" : 40,
                        "main" : 41,
                        "secondary" : 42,
                        },
                    "water-heating" : 43,
                },
            },
        },
    }

    def __init__(self,table):
        self.name = "hc"+table
        xlsname = f"{self.name}.xlsx"
        if not os.path.exists(xlsname):
            req = requests.get(f"{baseurl}{dataset}.xlsx")
            if req.status_code != 200:
                return None
            with open(xlsname,"wb") as f:
                f.write(req.content)
        self.book = openpyxl.load_workbook(xlsname)
        self.released_on = datetime.datetime.strptime(self.book['data']['A1'].value.split("\n")[0].split(":")[1].strip(),"%B %Y")
        self.revised_on = datetime.datetime.strptime(self.book['data']['A1'].value.split("\n")[1].split(":")[1].strip(),"%B %Y")

    def find(self,sheet,row=[],column=[]):
        book = self.book[sheet]
        rows = self.table_structure[self.name]["rows"]
        columns = self.table_structure[self.name]["columns"]
        while type(row) is list:
            rows = rows[row[0]]
            if len(row) > 1:
                row = row[1:]
            else:
                row = row[0]
        while type(column) is list:
            # print("Column:",column)
            columns = columns[column[0]]
            if len(column) > 1:
                column = column[1:]
            else:
                column = column[0]
        try:
            return book[f"{columns}{rows}"].value * self.table_structure[self.name]["units"]
        except:
            return rows,columns

class Microdata(pandas.DataFrame):

    def __init__(self):
        csvname = f"hc_raw.csv"
        if not os.path.exists(csvname):
            req = requests.get(microdata_url)
            if req.status_code != 200:
                return None
            with open(csvname,"wb") as f:
                f.write(req.content)
        pandas.DataFrame.__init__(self,pandas.read_csv(csvname))

import unittest

class _test(unittest.TestCase):

    def test_hc1_1(self):
        hc = HousingCharacteristics(table="1.1")
        self.assertEqual(hc.find('data',['total'],['total']),118.2e6)
        self.assertEqual(hc.find('data',['total'],['unit-type','single-family-detached']),73.9e6)
        self.assertEqual(hc.find('data',['fuel-used','natural-gas'],['total']),68.6e6)

    def test_microdata(self):
        md = Microdata()
        self.assertEqual(md["LPXBTU"][0],91.33)


if __name__ == "__main__":
    unittest.main()