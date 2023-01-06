import openpyxl
from pathlib import Path

# create book, sheet and add firts rows (columns name)

book = openpyxl.Workbook()
sheet = book["Sheet"]
sheet.title = "dados"
sheet.append(["usuario", "nome", "telefone", "email", "link externo"])

# set width of all columns

sheet.column_dimensions["A"].width = 22
sheet.column_dimensions["B"].width = 22
sheet.column_dimensions["C"].width = 22
sheet.column_dimensions["D"].width = 22
sheet.column_dimensions["E"].width = 22

# set font for first row (this method is deprecated)

sheet["A1"].font = sheet["A1"].font.copy(bold=True)
sheet["B1"].font = sheet["B1"].font.copy(bold=True)
sheet["C1"].font = sheet["C1"].font.copy(bold=True)
sheet["D1"].font = sheet["D1"].font.copy(bold=True)
sheet["E1"].font = sheet["E1"].font.copy(bold=True)

# add fake data for testings

for i in range(0,20):

    sheet.append(["redepitstopoficial", "Rede PitStop", "5545999970016", "","https://cobr.com.br/hrcorretoresdeimoveis"])

book.save(rf'{Path(__file__).parent}/username.xlsx')