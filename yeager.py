import csv 

from yconfig import yconfig
from finding import finding 
from data_reader import data_reader
from flight import flight
from flight import flight_activity
from flight import build_flight_list
from check_factory import * 


print("Initializing ------------------------------------------------")
config = yconfig("./config/cms_puf.yaml")
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
test_flights = build_flight_list(
    file_to_test._column_list,
    config.get_options(),
    findings)
print("Test Flight List Complete--------------------------")


print("Testing data--------------------------------------------")

# open the file and get ready to test each row
#
with open(file_to_test.filename()) as f:
    reader = csv.reader(f)
    #
    #   skip the first row because it iss the header
    #
    next(reader)
    line_counter = 0
    #
    #   for each record in the file
    #
    for current_rec in reader:
        line_counter +=  1
        # Verify number of columns in row
        # fatal error for row if not correct
        if len(current_rec) != config.number_of_columns():
            findings.add_finding(f"Row {line_counter}:Number of Columns Error skipping row. Expected:{config.number_of_columns()} Found:{len(current_rec)}")
            continue
        # valid row structure
        # apply tests to the appropriate columns
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
