import csv 
import re

from yconfig import yconfig
from finding import finding 
from data_reader import data_reader
print("Initializing ------------------------------------------------")
config = yconfig("./config/file.yaml")
#config.dump_yaml(False)
findings = finding(config.findings_filename())
print("Building reader --------------------------------------------")
# build data reader function
#print (f"Building data reader with :",config.input_filename(),config.input_filetype())
file_to_test = data_reader(config.input_filename(),config.input_filetype())

print("Verify Header --------------------------------------------")
#get header row
with open(file_to_test.filename()) as f:
    reader = csv.reader(f)
    for line  in reader:
        break
    file_to_test.set_column_list(line)

# dump header option
if config.dump_header():
    file_to_test.dump_column_list(True)

# verify number of columns
# Table Level: Number of Columns - Header           
if file_to_test.number_of_columns() == config.number_of_columns() :
    findings.add_finding("Number of columns matches!")
else:
    findings.add_finding("Number of columns don't match")
    findings.add_finding(f"Configured:{config.number_of_columns()}")
    findings.add_finding(f"Found in file: {file_to_test.number_of_columns()}")

print("Building Flight Plan--------------------------------")
flight_plan = []

for wstr in file_to_test._column_list:
    print("=====")
    print(f"Processing column : {wstr}")
    #print(config.get_options())
    for w in config.get_options():
        for k, v in w.items():
            #print(f"{k} contains {v}")
            #print(f"{v['name']}")
            if v['name'] == wstr:
                for z1,z2 in v.items():
                    print(f"{z1} is {z2}")

    






print("Testing data--------------------------------------------")
current_rec = []
line_counter = 1001
with open(file_to_test.filename()) as f:
    reader = csv.reader(f)
    for line  in reader:
        line_counter +=  1
        if line_counter == 1:
            field_list = line
            next

        # Verify number of columns in row
        current_rec = line
        if len(current_rec) != config.number_of_columns():
            findings.add_finding(f"Row {line_counter}:Number of Columns Error")

        if line_counter == config.dump_throttle() :
            break

findings.add_finding(f"Rows checked {line_counter}")


findings.dump_findings()


