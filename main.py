from database import DataBase
from tkui import TkUI
import sqlite3

a = DataBase()
a.add_paper({"PaperName":"howtomouyu","Publisher":"myself"})
a.modi_paper({"No":1,"Q0":"asdasd", "ReadOrNot":1})

# b = [{'No': 1, 'ReadOrNot': 0, 'PublicationYear': '', 'Publisher': '', 'Author': '', 'PaperName': 'howtomouyu', 'Tags': '', 'Notes': '', 'Url': '', 'Path': '', 'LastReadDate': '', 'Q0': 'asdasd', 'Q1': '', 'Q2': '', 'Q3': '', 'Q4': '', 'Q5': '', 'Q6': '', 'Q7': '', 'Q8': '', 'Q9': ''}]

print(a.show_all_paper())

TkUI(a)




