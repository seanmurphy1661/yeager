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
# dump header option
if config.dump_header():
    file_to_test.dump_column_list(True)
print("Verify Header --------------------------------------------")

# verify number of columns
# Table Level: Number of Columns - Header           
if file_to_test.number_of_columns() == config.number_of_columns() :
    findings.add_finding("Number of columns matches!")
else:
    findings.add_finding("Number of columns don't match")
    findings.add_finding(f"Configured:{config.number_of_columns()}")
    findings.add_finding(f"Found in file: {file_to_test.number_of_columns()}")
print(f"Header verified----------------------------------")


print("Building Flight Plan--------------------------------")
flight_plan = []
for w in config.get_options():
    # we have the name 
    # need position
    # test: option specified
    if "test" in w :
        
        # find the column number in file
        # by matching test.name to data_reader.column[]
        if w['test']['name'] in file_to_test._column_list:
            n = file_to_test._column_list.index(w['test']['name'])
        else:
            # can't fly with out the number
            print(f"column not found {w['test']['name']}")
            findings.add_finding(f"column not found {w['test']['name']}")
            next
        # column name and position in file are determined
        # create the flight object
        working_flight = flight(w['test']['name'], n)
        
        #
        # add regex flight test to the working flight
        if 'regex' in w['test']:
            working_flight.append_test(generate_regex_check("",w['test']['regex']))

        # all the flight tests are in, file the flight in the book
        flight_plan.append(working_flight)

print("Flight plan complete---------------------------")


print("Testing data--------------------------------------------")
current_rec = []
line_counter = 0

# open the file and get ready to test each row
#
with open(file_to_test.filename()) as f:
    reader = csv.reader(f)
    for current_rec in reader:
        line_counter +=  1
        # Verify number of columns in row
        # fatal error for row
        if len(current_rec) != config.number_of_columns():
            findings.add_finding(f"Row {line_counter}:Number of Columns Error skipping row")
            next

        # apply tests in flightplan to the appropriate columns
        # 
        for i in range(0,len(flight_plan)):
            # each flight in the flightplan has flight tests
            # execute each one on the appropriate column  
            if len(flight_plan[i].flight_test_array):
                result = flight_plan[i].flight_test_array[0](current_rec[flight_plan[i].flight_number])
                if not result:
                    findings.add_finding(f"Test failed:{line_counter}:{flight_plan[i].flight_name}:{current_rec[working_result]}")

        # throttle test, 0 = no limit
        if config.dump_throttle() != 0 and line_counter == config.dump_throttle() :
            break

print("Testing data complete-------------------------------------------")

print("Wrapping up ------------------------------------")
findings.add_finding(f"Rows checked {line_counter}")

findings.dump_findings()

print("Done. ----------------------------------")
