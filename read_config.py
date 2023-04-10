import csv 
import re

from yconfig import yconfig
from finding import finding 
from data_reader import data_reader
from flight import flight
from flight import flight_activity
from check_factory import * 


print("Initializing ------------------------------------------------")
config = yconfig("./config/file.yaml")
if config.dump_config():
    config.dump_yaml(False)
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


print("Building Test Flight List--------------------------------")
# s/b function / class to encasulate this process
# required inputs:
#   config.get_options - provides the list of requested tests
#   file_to_test.column_list - provides the column name lookup for position
#
test_flights = []
for w in config.get_options():
    # we have the name 
    # need position
    # test: option specified
    if "test" in w :
        
        # find the column number in file
        # by matching test.name to data_reader.column[]
        if w['test']['name'] in file_to_test._column_list:
            column_number = file_to_test._column_list.index(w['test']['name'])
        else:
            # can't fly with out the number
            print(f"column not found {w['test']['name']}")
            findings.add_finding(f"column not found {w['test']['name']}")
            next
            
        # column name and position in file are determined
        # create the flight object
        working_flight = flight(w['test']['name'], column_number)
        
        #
        # add regex flight test to the working flight
        if 'regex' in w['test']:
            working_flight.append_flight_activity(flight_activity(
                "regex test",
                f"column failed regex test {w['test']['regex']}",
                generate_regex_check("",w['test']['regex'])))

        #if 'range' in w['test']:
        #    print(f"Range test: Low value = {w['test']['range'][0]}")
        #    working_flight.append_flight_activity(generate_range_check(0,w['test']['range'][0],w['test']['range'][1]))

        # all the flight tests are in, file the flight in the book
        test_flights.append(working_flight)

print("Test Flight List Complete--------------------------")


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
        # fatal error for row if not correct
        if len(current_rec) != config.number_of_columns():
            findings.add_finding(f"Row {line_counter}:Number of Columns Error skipping row")
            next

        # apply tests in flightplan to the appropriate columns
        # 
        for i in test_flights:
            # each flight has flight test activities
            # execute each one on the appropriate column  
            if len(i.flight_activities):
                for j in i.flight_activities:
                    print(f"Activity name: {j.flight_activity_name}")
start here-> 

                    # result = j.activity(current_rec[i.flight_number])
                    result = True
                    if not result:
                        findings.add_finding(f"Test failed:Row:{line_counter}:Flight Name:{test_flights[i].flight_name}:Row Value:{current_rec[test_flights[i].flight_number]}")
                        break 

        # throttle test, 0 = no limit
        if config.dump_throttle() != 0 and line_counter == config.dump_throttle() :
            break

print("Testing data complete---------------------------")

print("Wrapping up ------------------------------------")
findings.add_finding(f"Rows checked {line_counter}")
findings.record_findings()
print("Done. ------------------------------------------")
