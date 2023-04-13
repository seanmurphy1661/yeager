import csv 

from yconfig import yconfig
from finding import finding 
from data_reader import data_reader
from flight import flight
from flight import flight_activity
from check_factory import * 


print("Initializing ------------------------------------------------")
config = yconfig("./config/file.yaml")
if config.dump_config():
    config.dump_yaml(True)
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
#   findings - in the odd case there are issuess we'd like 
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
        #
        # add range flight activity to working flight
        if 'range' in w['test']:
            print(f"Range test: Low value = {w['test']['range'][0]}")
            working_flight.append_flight_activity(flight_activity(
                "range test",
                f"column failed range test {w['test']['range'][0]},{w['test']['range'][1]}",
                generate_range_check(0,w['test']['range'][0],w['test']['range'][1])))
         #
         # add type flight activity to working flight
         # all flights start as string
         #
        if 'type' in w['test']:
            print(f"Type check:{w['test']['type']}")
            if w['test']['type'] == 'date':
                working_flight.update_type("date")
                working_flight.append_flight_activity(flight_activity(
                    "date type check",
                    "column failed date check",
                    generate_date_type_check("")))
            elif w['test']['type'] == 'number':
                working_flight.update_type("number")
                working_flight.append_flight_activity(flight_activity(
                    "number type check",
                    "column failed number check",
                    generate_number_type_check(0)
                ))

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
        for flight in test_flights:
            # each flight has flight test activities
            # execute each one on the appropriate column  
            if len(flight.flight_activities):
                for flight_activity in flight.flight_activities:
                    result = flight_activity.flight_activity(current_rec[flight.flight_number])
                    if not result:
                        findings.add_finding(f"Row:{line_counter}:Test failed:{flight_activity.flight_activity_message}:Flight Name:{flight.flight_name}:Row Value:{current_rec[flight.flight_number]}")
                        break 

        # throttle test, 0 = no limit
        if config.dump_throttle() != 0 and line_counter == config.dump_throttle() :
            break

print("Testing data complete---------------------------")

print("Wrapping up ------------------------------------")
findings.add_finding(f"Rows checked {line_counter}")
findings.record_findings()
print("Done. ------------------------------------------")
