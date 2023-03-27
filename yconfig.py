import yaml

class yconfig:
    """Encapsulates Configurations"""

    def __init__(self,filename):
        """Initialize object with filename"""
        self._filename = filename
        with open(filename,"r") as stream:
            try:
                self.yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def column_delimiter(self):
        return self.yaml['column_delimiter']
    
    def filename(self):
        """Return Filename"""
        return self._filename
    
    def yaml(self):
        """Return the raw yaml config"""
        return self.yaml

    def dump_yaml(self):
        """send raw config to stdout"""
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
        
    def input_filename(self):
        return self.yaml['input_filename']
    
    def findings_filename(self):
        return self.yaml['findings_filename']