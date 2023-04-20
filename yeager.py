import argparse
import csv 

from yconfig import yconfig
from finding import finding 
from data_reader import data_reader
from flight import flight
from flight import flight_activity
from flight import build_flight_list
from check_factory import * 

def main():
    print("Initializing ---------------------------------------------")

    parser = argparse.ArgumentParser(
        prog='yeager',
        description='run qa tests against data files',
        epilog='quality is job #1')
    parser.add_argument('filename')
    args = parser.parse_args()
    config = yconfig(args.filename)
    if not config.yaml_loaded:
        print(f"Configuration file {args.filename} could not be loaded.")
        return (1)
    
    if config.dump_config():
        config.dump_yaml(True)
    findings = finding(config.findings_filename())

    print("Building reader -----------------------------------------")

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
    print(f"Header verified ------------------------------------------")


    print("Building Test Flight List ---------------------------------")
    test_flights = build_flight_list(
        file_to_test._column_list,
        config.get_options(),
        findings)
    print("Test Flight List Complete ---------------------------------")


    print("Testing data ----------------------------------------------")

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
            for flight in test_flights:

                # check to see if data is present to test
                if len(current_rec[flight.flight_number]) == 0:
                    #  when data is required, create a finding 
                    if flight.flight_data_required == True:
                        findings.add_finding(f"Row:{line_counter}:Test failed: data required:Flight Name:{flight.flight_name}:{current_rec[flight.flight_number]}")
                
                else:
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

if __name__ == "__main__":
    main()
