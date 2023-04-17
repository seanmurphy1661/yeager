# Yeager 
-----

Data testing with Python.

Yeager uses a yaml file to define the files to be tested and the tests to apply to each column.

## file.yaml
file.yaml is the name of the file that is used to define the tests and file to be tested.

  ### File settings

*input_filename:* specified the file to be tested

*input_filetype:* specifies the type of file
- "csv"

*column_delimiter:* used to separate columns in a row
- any valid character

*number_of_columns:* used to verify row size

  
### Control settings
*dump_throttle:* specified the number of rows to check
- Use 0 to disable 

*dump_header:* contols printing header row

*dump_config:* contols print config from file.yaml

### Reporting
*findings_filename:* any valid file name that can be written to disk.
  
## commands
 Commands are specified in the options list in file.yaml. 

### test command

*name:* name of column that will be tested. 
- for csv files, a column in the header must match or the entire test is rejected

*regex:* a regular expression compatible with the Python pe library.

*type:* specifies a datatype check. default datatype is string. Valid types:
- date - use dateutil.parse to check for date datatype conformance
- number - use regex to verify number data type
- money - use regex to verify money format

*range:* specifies a numeric range 
- range is specified as an array '[min,max]'

## Example file.yaml
```
option:
  - test: 
      name: column_to_test
      regex: "^[0-9]{1,2}$"
      range: [2,99]
```
*Testing for a number between 2 and 99.*
  
## Appendix
### Common expressions
- *Number :* '^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$'
- *BinaryChoice :* "^Choice 1$|^Choice 2$"
- *Integer:* "^(0|[1-9][0-9]*)$"
- *Two digit code, Not required:* "^[0-9]{0,2}$"

# Autoflight
## Analyzes sample file and builds the yeager.yaml file
