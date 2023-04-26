#!/usr/bin/env python3

import csv
import re

dbob_years = [2014, 2015, 2016, 2018, 2019, 2021, 2022]
dbob_columns = ['Name wie von SEC verwendet']
for y in dbob_years:
  dbob_columns.append(str(y) + ' Don’t Bank on the Bomb')

dbob = {}
with open('dbob.csv', 'r') as f:
  reader = csv.DictReader(f)
  for row in reader:
    names = []
    for column in dbob_columns:
      if row[column] != "":
        names.append(row[column])
    dbob[names[0]] = row
    dbob[names[0]]['names'] = names
    # treating dates of the format yyyymmdd as numbers for comparison purposes
    dbob[names[0]]['dbob_from'] = 99999999
    dbob[names[0]]['dbob_to']   = 00000000
    for y in dbob_years:
      if(row[str(y) + ' Don’t Bank on the Bomb'] != ""):
        dbob[names[0]]['dbob_from'] = y * 10000
        break
    for y in dbob_years:
      if(row[str(y) + ' Don’t Bank on the Bomb'] != ""):
        dbob[names[0]]['dbob_to'] = y * 10000 + 1231

results = [["Datum", "CH-Firma investiert in...", "Anlage mit diesem ISIN", "und diesem Namen", "Wert in CHF"]]
for d in ["31.12.2021", "30.12.2022"]:
  with open("compenswiss - list of positions - " + d + ".csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
      match = False
      canonicalName = None
      for key in dbob:
        if(dbob[key]['2022 Don’t Bank on the Bomb'] != ""):
          for name in dbob[key]['names']:
            r = re.search(name, row['Description'], re.IGNORECASE)
            if(r):
              match = True
              canonicalName = key
      
      if(match):
        results.append([d, "AHV", row['ISIN'], canonicalName, int(row['Market Value CHF'].replace("'", ""))])

with open('results.csv', 'w', newline='') as f:
  csv.writer(f).writerows(results)