import csv 

from yconfig import yconfig
from finding import finding 

def printit(): print("im here")


config = yconfig("./config/file.yaml")
config.dump_yaml(True)
findings = finding(config.findings_filename())

field_list = []
current_rec = []
line_counter = 0
with open(config.input_filename()) as f:
    reader = csv.reader(f)
    for line  in reader:
        line_counter +=  1
        if line_counter == 1:
            field_list = line
            #
            # Table Level: Number of Columns - Header 
            print(f"Number of Columns: {len(field_list)}")
            if len(field_list) == config.number_of_columns() :
                findings.add_finding("Number of columns matches!")
            else:
                findings.add_finding("Number of columns don't match")

            if config.dump_header():
                for wstr in field_list:
                    print(wstr)

                print('**************************')
                for i in range(0,config.number_of_columns()):
                    print(field_list[i])

                print('**************************')
                printit()
            next

        current_rec = line
        if len(current_rec) != config.number_of_columns():
            finding.add_finding(f"Row {line_counter}:Number of Columns Error")

        if line_counter == config.dump_throttle() :
            break

findings.add_finding(f"Rows checked {line_counter}")
print("Findings")
findings.dump_findings()


