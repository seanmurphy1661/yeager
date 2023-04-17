import yaml
import csv

filename = "./testdata/cms_puf.csv"
delimiter = ","
output_filename = "./config/csm_puf.yaml"
findings_filename = "cms_puf.findings"
number_of_columns = 0
column_name = []
min_max = []
column_type = []
column_type_change = []
width=[]

row_count = 0 
with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    for current_rec in reader:
        row_count += 1 
        print(f"row: {row_count}")
        if row_count == 1:
            number_of_columns = len(current_rec)
            # output_lines=[]
            # output_lines.append(f"# generated by yeager")
            # output_lines.append(f"# {output_filename}")
            # output_lines.append(f"input_filename: \"{filename}\"")
            # output_lines.append(f"input_filetype: \"csv\"")
            # output_lines.append(f"dump_throttle: 0")
            # output_lines.append(f"dump_header: False")
            # output_lines.append(f"dump_config: False")
            # output_lines.append(f"column_delimiter: \"{delimiter}\"")
            # output_lines.append(f"number_of_columns: {number_of_columns}")
            # output_lines.append(f"findings_filename: \"{findings_filename}\"")
            # output_lines.append(f"\noptions:")
            for str in current_rec:
                # output_lines.append(f"  - test:")
                # output_lines.append(f"      name: {str}")
                column_name.append(str)
                column_type.append("string")
                column_type_change.append(0)
                width.append([0,0])
        else:
            for i in range(0,number_of_columns-1):
                if len(current_rec[i]) > width[i][1]:
                    width[i] = len(current_rec[i])
                
                

# with open(output_filename,"w") as o:
#     for w in output_lines:
#         print(w,file=o)
                
for i in range(0,number_of_columns-1):
    print(f"col: {column_name[i]} width:{width[i]}")

