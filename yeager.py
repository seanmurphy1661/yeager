import argparse

from yconfig import yconfig
from finding import finding 
from data_reader import data_reader
from flight import build_flight_list
from activity_factory import * 

def main():
    print("Initializing ----------------------------------------------")

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
    print(f"{config.stats_enabled()}")

    if config.dump_config():
        config.dump_yaml(True)
    findings = finding(config.findings_filename())

    print("Building reader -------------------------------------------")

    # build data reader function
    file_to_test = data_reader(config.input_filename(),config.input_filetype())
    # dump header option
    if config.dump_header():
        file_to_test.dump_column_list(True)

    print("Verify Header ---------------------------------------------")

    # verify number of columns
    # Table Level: Number of Columns - Header           
    if file_to_test.number_of_columns() == config.number_of_columns() :
        findings.add_finding("Number of columns matches!")
    else:
        findings.add_finding("Number of columns don't match")
        findings.add_finding(f"Configured:{config.number_of_columns()}")
        findings.add_finding(f"Found in file: {file_to_test.number_of_columns()}")

    print("Header verified -------------------------------------------")
    print("Building Test Flight List ---------------------------------")

    test_flights = build_flight_list(
        file_to_test._column_list,
        config.get_options(),
        findings)
    
    print("Test Flight List Complete ---------------------------------")
    print("Testing data ----------------------------------------------")

    # test the file with the set of flights and where to report
    file_to_test.flight_test(test_flights,config,findings)

    print("Testing data complete -------------------------------------")
    print("Wrapping up -----------------------------------------------")
    
    findings.record_findings()

    print("Done. -----------------------------------------------------")

if __name__ == "__main__":
    main()
