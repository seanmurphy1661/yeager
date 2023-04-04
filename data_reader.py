import csv

class data_reader:
    """Encapsulates the details of getting data"""

    def __init__(self,filename,type):
        self._filename = filename
        self._number_of_columns = 0
        self._type = type
        self._last_line=[]
        #open file and load header
        with (open(filename)) as f:
            reader = csv.reader(f)
            for line in reader:
                break
            self._column_list = line
            self._number_of_columns = len(line)
        

    def set_column_list(self,column_list):
        self._column_list = column_list
        self._number_of_columns = len(column_list)
        return self._column_list
    
    def dump_column_list(self,pretty):
        if pretty:
            print("Pretty Column List")
            for wstr in self._column_list:
                print(" ",wstr)
        else:
            print(self._column_list)
    
    def filename(self):
        return self._filename
    
    def number_of_columns(self):
        return self._number_of_columns
    
    
    