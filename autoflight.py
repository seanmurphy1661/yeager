import argparse
import csv
import re 
from os.path import exists
#
def main():
    parser = argparse.ArgumentParser(
        prog='autoflight',
        description='create a yeager config file from sample data',
        epilog='quality is job #1')
    parser.add_argument('targetname',help="The file to analyze.")
    parser.add_argument('-d','--delimiter',dest="delimiter",default=",",help="Column delimiter column. Comma (,) is the default.")
    parser.add_argument('-c','--config',dest="output_filename",help="Name of the yeager config file.",required=True)
    parser.add_argument('-s','--sample_size',dest="sample_size",help="Number of records to sample before creating config",required=False)
    parser.add_argument('-o','--overwrite', action='store_true', dest="overwrite_flag", help="Overwrite if configuration exists")
    args = parser.parse_args()

    print("Initializing ----------------------------------------------")
    filename = args.targetname
    delimiter = args.delimiter

    if args.output_filename :
        output_filename = args.output_filename.strip()
    else:
        output_filename = f"{args.targetname}.yeager.yaml"

    if args.overwrite_flag:
        overwrite_flag = True
    else:
        overwrite_flag = False

    sample_size = 0
    if args.sample_size:
        pe = re.compile("^(0|[1-9][0-9]*)$")
        if pe.match(args.sample_size.strip()) != None:
            sample_size = int(args.sample_size.strip())

 
    print(f"Target file: {filename}")
    print(f"Delimiter: {delimiter}")
    print(f"Output configuration: {output_filename}")
    print(f"Overwrite flag: {overwrite_flag}")
    print(f"Sample size: {sample_size}")
    print("Complete ----------------------------------------------")
    
    if exists(output_filename) and not overwrite_flag:
        print(f"File exists. quitting.")
        print("Use -o to overwrite existing configuration")
        return(1)
    #
    # number of columns is based on the header
    number_of_columns = 0
    # list of column names
    column_name = []
    # column_types - default to string
    column_type = []
    # required - are zero-len strings allowed
    column_empty_count=[]
    column_required=[]
    # column width [min,max]
    width=[]
    #
    #   count the number of rows that conform to a number regex
    column_number_type = []
    # 
    #   re pattern for testing numeric
    number_re = re.compile('^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$') 
    #
    #   count the number of rows in the test file
    #   row_count is the denominator for data type infrence
    row_count = 0 
    print("Processing ----------------------------------------------")

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for current_rec in reader:
            row_count += 1 
            if row_count == 1:
                #
                # first time initialization
                number_of_columns = len(current_rec)
                for str in current_rec:
                    column_name.append(str)
                    column_type.append("string")
                    column_number_type.append(0)
                    column_empty_count.append(0)
                    column_required.append(False)
                    width.append([0,0])
            else:
                for i in range(0,number_of_columns-1):
                    #
                    #   Update minimum and maximum widths
                    #
                    # width[0] = minimum
                    # width[1] = maximum
                    if len(current_rec[i]) > width[i][1]:
                        width[i][1] = len(current_rec[i])
                        if width[i][0] == 0:
                            width[i][0] = len(current_rec) 
                    if len(current_rec[i]) < width[i][0]:
                        width[i][0] = len(current_rec[i])
                    #
                    # part of the type calculation
                    # if data matches a number lets add one to the evidence
                    if number_re.match(current_rec[i]):
                        column_number_type[i] += 1
                    #
                    # count empty rows with empty column for
                    # required tag later
                    if len(current_rec[i]) == 0 :
                        column_empty_count[i] += 1

            if sample_size > 0 and row_count == sample_size:
                break

    # 
    # post processing
    #                 
    # step 1 type processing
    # check the evidence for a number type
    print(f"Rows processed: {row_count}")
    print("Post Processing ----------------------------------------------")

    for i in range(0,number_of_columns-1):
        working_pct = column_number_type[i]/row_count
        if working_pct > .75 :
            column_type[i] = "number"
        if column_empty_count[i] == 0 :
            column_required[i] = True
        

    #
    # create yaml file
    #
    print("Output ----------------------------------------------")
    output_lines=[]
    output_lines.append(f"# generated by autoflight")
    output_lines.append(f"# {output_filename}\n")
    output_lines.append(f"input_filename: \"{filename}\"")
    output_lines.append(f"input_filetype: \"csv\"")
    output_lines.append(f"dump_throttle: 0")
    output_lines.append(f"dump_header: False")
    output_lines.append(f"dump_config: False")
    output_lines.append(f"column_delimiter: \"{delimiter}\"")
    output_lines.append(f"number_of_columns: {number_of_columns}")
    output_lines.append(f"findings_filename: \"{output_filename}.findings\"")

    output_lines.append(f"\nstats:")
    output_lines.append(f"  enabled: False")
    output_lines.append(f"  file: \"{output_filename}.stats\"")
    output_lines.append(f"  report: \"{output_filename}.report\"")
                        
    output_lines.append(f"\noptions:")

    for i in range(0,number_of_columns-1):
        output_lines.append(f"  - test:")
        output_lines.append(f"      name: {column_name[i]}")
        output_lines.append(f"      type: {column_type[i]}")
        output_lines.append(f"      width: {width[i]}")
        output_lines.append(f"      required: {column_required[i]}")

    with open(output_filename,"w") as o:
        for w in output_lines:
            print(w,file=o)
    print("Done ----------------------------------------------")


if __name__ == "__main__":
    main()