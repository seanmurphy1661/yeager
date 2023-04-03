import csv 
import re

from yconfig import yconfig
from finding import finding 
from data_reader import data_reader
from flight import flight
from check_factory import * 


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
for w in config.get_options():
    print(w)
    # we have the name 
    # need position
    if w['test']['name'] in file_to_test._column_list:
        print(file_to_test._column_list.index(w['test']['name']))
        n = file_to_test._column_list.index(w['test']['name'])
    else:
        print(f"column not found {w['test']['name']}")
        findings.add_finding(f"column not found {w['test']['name']}")
        next

    working_flight = flight(w['test']['name'], n)
    
    if 'regex' in w['test']:
        print(f"Create regex {w['test']['regex']}")

        working_flight.append_test(generate_regex_check("",w['test']['regex']))

    flight_plan.append(working_flight)

print("Flight plan complete---------------------------")


print("Testing data--------------------------------------------")
current_rec = []
line_counter = 0
with open(file_to_test.filename()) as f:
    reader = csv.reader(f)
    for current_rec in reader:
        line_counter +=  1
        # Verify number of columns in row
        # fatal error for row
        if len(current_rec) != config.number_of_columns():
            findings.add_finding(f"Row {line_counter}:Number of Columns Error")
            next

        for i in range(0,len(flight_plan)):
            #print(flight_plan[i].flight_name)
            #print(flight_plan[i].flight_number)
            #print(len(flight_plan[i].flight_test_array))
            if len(flight_plan[i].flight_test_array):
                working_result = flight_plan[i].flight_number
                result = flight_plan[i].flight_test_array[0](current_rec[working_result])
                if not result:
                    findings.add_finding(f"Test failed:{line_counter}:{flight_plan[i].flight_name}:{current_rec[working_result]}")
                print(result)
        






        if line_counter == config.dump_throttle() :
            break



findings.add_finding(f"Rows checked {line_counter}")

findings.dump_findings()


