import yaml

class yconfig:
    """Encapsulates Configurations"""

    def __init__(self,filename):
        """Initialize object with filename"""
        # filename is the name of the configuration file
        # see inputfile for name of file being tested
        self._filename = filename
        self.yaml_loaded = False
        try:
            with open(filename,"r") as stream:
                try:
                    self.yaml_contents = yaml.safe_load(stream)
                    self.yaml_loaded = True
                except yaml.YAMLError as exc:
                    print(exc)
        except FileNotFoundError as exc:
            print(exc)
# 
#   runtime statistics
# 
    def stats_enabled(self):
        rv = False
        if 'stats' in self.yaml_contents:
            if 'enabled' in self.yaml_contents['stats']:
                if self.yaml_contents['stats']['enabled'] == True:
                    rv = True
        return rv
    
    # raw stats file
    def stats_file(self):
        rv=""
        if 'stats' in self.yaml_contents:
            if 'file' in self.yaml_contents['stats']:
                rv = self.yaml_contents['stats']['file']
        return rv
    
    # text report
    def stats_report(self):
        rv=""
        if 'stats' in self.yaml_contents:
            if 'file' in self.yaml_contents['stats']:
                rv = self.yaml_contents['stats']['file']
        return rv
    # 
    #   Input File Properties
    # 
    def column_delimiter(self):
        rv = ","
        if 'column_delimiter' in self.yaml_contents:
            rv = self.yaml_contents['column_delimiter']
        return rv

    def input_filename(self):
        rv = "input.csv"
        if 'input_filename' in self.yaml_contents:
            rv = self.yaml_contents['input_filename']
        return rv
    
    def input_filetype(self):
        """Return filetype"""
        rv = "csv"
        if 'input_filetype' in self.yaml_contents:
            if self.yaml_contents['input_filetype'] != 'csv':
                rv = 'csv'
            else:
                rv = self.yaml_contents['input_filetype']
        return rv


    def filename(self):
        """Return Filename"""
        # name of config file
        return self._filename

    def yaml(self):
        """Return the raw yaml config"""
        return self.yaml
    #
    #   output control
    #
    def dump_config(self):
        '''return the setting to display config'''
        rv = False
        if 'dump_config' in self.yaml_contents:
            if self.yaml_contents['dump_config'] == True:
                rv = True 
        return rv
    
    def dump_throttle(self):
        rv = 0
        if 'dump_throttle' in self.yaml_contents:
            rv = self.yaml_contents['dump_throttle']
        return rv 
    
    def dump_header(self):
        rv = False
        if 'dump_header' in self.yaml_contents:
            if self.yaml_contents['dump_header'] == True :
                rv = True
        return rv
    
    def dump_flight(self):
        rv = False
        if 'dump_flight' in self.yaml_contents:
            if self.yaml_contents['dump_flight'] == True :
                rv = True
        return rv
    #
    # number of columns
    #
    def number_of_columns(self):
        rv = 0
        if 'number_of_columns' in self.yaml_contents:
            rv = self.yaml_contents['number_of_columns']
        return rv
    #
    #
    #
    def findings_filename(self):
        rv = "yeager.findings"
        if 'findings_filename' in self.yaml_contents:
            rv =  self.yaml_contents['findings_filename']
        return rv
    
    #
    # options
    #
    def options(self):
        return self.yaml_contents['options']

    def get_options(self):
        return self.yaml_contents['options']
    
# 
#   Methods
#       
    def dump_yaml(self,pretty):
        """send raw config to stdout"""
        if pretty:
            print("*******************************************")
            print(f"Using config: {self._filename}")
            print(f"Throttle at: {self.dump_throttle()}")
            print(f"Column Delimiter: {self.column_delimiter()}")
            print(f"Input file: {self.input_filename()}")
            print(f"Findings file: {self.findings_filename()}")
            print("*******************************************")
        else:
            print(self.yaml)
