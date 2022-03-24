import configparser, os

from database import DataBase
from tkui import TkUI

import sqlite3

SETTING_PATH = ".\\setting.conf"

conf = configparser.ConfigParser()
if not os.path.isfile(SETTING_PATH):
    conf.add_section("default")
    conf.set("default","pdf_reader", "D:\\tools\\Foxit\\FoxitPhantomPDF.exe")
    conf.write(open(SETTING_PATH, "w"))
else:
    conf.read(SETTING_PATH, encoding="utf-8")

# print(conf.sections())
# print(conf.get("default", "pdf_reader"))


a = DataBase()
print(a.show_all_paper())
TkUI(a, conf)



# a.add_paper({"PaperName":"howtomouyu","Publisher":"myself"})
# a.modi_paper({"No":1,"Q0":"asdasd", "ReadOrNot":1})

# b = [{'No': 1, 'ReadOrNot': 0, 'PublicationYear': '', 'Publisher': '', 'Author': '', 'PaperName': 'howtomouyu', 'Tags': '', 'Notes': '', 'Url': '', 'Path': '', 'LastReadDate': '', 'Q0': 'asdasd', 'Q1': '', 'Q2': '', 'Q3': '', 'Q4': '', 'Q5': '', 'Q6': '', 'Q7': '', 'Q8': '', 'Q9': ''}]






