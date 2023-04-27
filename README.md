<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Yeager is a framework for performing quality tests on data files. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

This code has been developed and tested with Python 3.11 

### Depenency List
* Python version 3.11 or later
  
### Installation

1. Navigate to https://github.com/seanmurphy1661/yeager
2. Clone the repo
   ```sh
   git clone https://github.com/seanmurphy1661/yeager.git
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Autoflight
Analyzes sample file and builds a yaml file that can be used for testing production files.

```
autoflight.py filename [-c|--config configfile] [-d|--delimiter delimiter]
```

### Yeager
Verifies files against a set of tests defined in the *configfile*.

```
yeager.py configfile
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Configuration
The configuration file, aka *configfile*, is a specification for the tests that will be preformed against the file named in *input_filename*.
As shown below, the configuration file also includes processing directives that govern processing. 

Autoflight.py will create a fully functional configuration file. This is particularly helpfull for files with many columns. 

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
*findings_filename:* any valid file name that can   

### Test Options 
*name:* name of column that will be tested. 
- for csv files, a column in the header must match or the entire test is rejected

*range:* specifies a numeric range 
- range is specified as an array '[min,max]'

*regex:* a regular expression compatible with the Python pe library.

*required:* specifies if content must be present
- True: Zero length strings are flagged as a finding
- False: Zero length strings are allowed

*width:* specifies column size properties
- width is specified as an array '[min,max]'

*type:* specifies a datatype check. default datatype is string. Valid types:
- string - no validation
- date - use dateutil.parse to check for date datatype conformance
- number - use regex to verify number data type
- money - use regex to verify money format

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Appendix
## Example file.yaml
```
input_filename: "file_to_test.csv"
input_filetype: "csv"
dump_throttle: 0
dump_header: True
dump_config: True
column_delimiter: ","
number_of_columns: 10
findings_filename: "file_to_test.csv.findings"

option:
  - test: 
      name: column_to_test
      regex: "^[0-9]{1,2}$"
      range: [2,99]
  .
  .
  .

```
*Testing for a number between 2 and 99.*
<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
### Common expressions
- *Number :* '^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$'
- *BinaryChoice :* "^Choice 1$|^Choice 2$"
- *Integer:* "^(0|[1-9][0-9]*)$"
- *Two digit code, Not required:* "^[0-9]{0,2}$"
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the GNU GENERAL PUBLIC LICENSE. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Best README Template: https://github.com/othneildrew/Best-README-Template

<p align="right">(<a href="#readme-top">back to top</a>)</p> 
