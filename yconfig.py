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
                    self.yaml = yaml.safe_load(stream)
                    self.yaml_loaded = True
                except yaml.YAMLError as exc:
                    print(exc)
        except FileNotFoundError as exc:
            print(exc)


    def column_delimiter(self):
        return self.yaml['column_delimiter']
    
    def filename(self):
        """Return Filename"""
        # name of config file
        return self._filename

    def yaml(self):
        """Return the raw yaml config"""
        return self.yaml

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

    def dump_throttle(self):
        return self.yaml['dump_throttle']
    
    def number_of_columns(self):
        return self.yaml['number_of_columns']
    
    def options(self):
        return self.yaml['options']

    def dump_header(self):
        if self.yaml['dump_header'] == True :
            return True
        else:
            return False
        
    def suppress_findings(self):
        return self.yaml['suppress_findings']

    def dump_config(self):
        if self.yaml['dump_config'] == True:
            return True
        else:
            return False
        
    def input_filename(self):
        return self.yaml['input_filename']
    
    def input_filetype(self):
        """Return filetype"""
        return self.yaml['input_filetype']

    def findings_filename(self):
        return self.yaml['findings_filename']
    
    def get_options(self):
        return self.yaml['options']