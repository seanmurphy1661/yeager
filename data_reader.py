import csv

class data_reader:
    """Encapsulates the details of getting data"""

    def __init__(self,filename,type) -> None:
        self._filename = filename
        self._type = type
        self._last_line=[]
        self._column_list=[]
        with open(filename,"r") as stream:
            self._column_list = csv.reader(stream)

            print(self._column_list)


    def get_column_list(self):
        return self._column_list
    
