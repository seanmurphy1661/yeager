-----
Data testing with Python.

Yeager uses a yaml file to define the files to be tested and the tests to apply to each column.

  
  

## file.yaml
file.yaml is the name of the file that is used to define the tests and file to be tested.

  

### File settings

**input_filename:** specified the file to be tested

**input_filetype:** specifies the type of file

- "csv"

**column_delimiter:** used to separate columns in a row

- any valid character

**number_of_columns:** used to verify row size

  

## control settings

dump_throttle: specified the number of rows to check 0

dump_header: off

dump_config: off

  

## reporting

findings_filename: "findings.txt"

  

## commands

  

Commands are specified in the options list in file.yaml.

  

## command test

- test

  

regex: string

regex - create python regular expression using supplied string

  

common strings

- Money :

- Number : '^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$'

- BinaryChoice : "^National$|^State$"

- Integer: "^(0|[1-9][0-9]*)$"

- Zipcode:

- Email:

- Two digit code, Not required: "^[0-9]{0,2}$"

- State Abbreviation: "^(A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]|PA|RI|S[CD]|T[NX]|UT|V[AT]|W[AIVY])$

  

-

  

Specialized
