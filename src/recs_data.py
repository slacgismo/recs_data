import os, sys
import openpyxl
import requests

baseurl = "https://www.eia.gov/consumption/residential/data/2015/hc/"
sources = {
    "2015" : {
        "hc1.1" : "by Housing unit type (HC1.1)",
        "hc1.2" : "by Owner/renter status (HC1.2)",
    }
}

def hc_load(dataset):
    xlsname = f"{dataset}.xlsx"
    if not os.path.exists(xlsname):
        req = requests.get(f"{baseurl}{dataset}.xlsx")
        if req.status_code != 200:
            return None
        with open(xlsname,"wb") as f:
            f.write(req.content)
    data = openpyxl.load_workbook(xlsname)
    return data

import unittest

class _test(unittest.TestCase):

    def test_hc1_1(self):
        xls = hc_load("hc1.1")
        self.assertTrue(xls)