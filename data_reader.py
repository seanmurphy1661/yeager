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

    #
    #   flight_test - apply the test_flights to the current data reader object (file to test)
    #   inputs: 
    #           test_flights object
    #           config object
    #           findings object
    #
    def flight_test(self,test_flights,config,findings):
        #
        if config.stats_enabled:
            print(f"stats on") 
        #
        #   open the file
        #
        with open(self.filename()) as f:
            reader = csv.reader(f)
            #
            #   skip the first row because it is the header
            #
            next(reader)
            line_counter = 0
            #
            #   for each record in the file
            #
            for current_rec in reader:
                line_counter +=  1
                
                # Verify number of columns in row
                # fatal error for row if not correct
                if len(current_rec) != config.number_of_columns():
                    findings.add_finding(f"Row {line_counter}:Number of Columns Error skipping row. Expected:{config.number_of_columns()} Found:{len(current_rec)}")
                    continue


                # we have a valid row structure
                # apply tests to the appropriate columns
                for flight in test_flights:

                    # check to see if data is present to test
                    if len(current_rec[flight.flight_number]) == 0:
                        #  when data is required, create a finding 
                        if flight.flight_data_required == True:
                            findings.add_finding(f"Row:{line_counter}:Test failed: data required:Flight Name:{flight.flight_name}:{current_rec[flight.flight_number]}")
                    
                    else:
                        # each flight has flight test activities
                        # execute each one on the appropriate column
                        if len(flight.flight_activities):
                            for flight_activity in flight.flight_activities:
                                result = flight_activity.flight_activity(current_rec[flight.flight_number])
                                if not result:
                                    findings.add_finding(f"Row:{line_counter}:Test failed:{flight_activity.flight_activity_message}:Flight Name:{flight.flight_name}:Row Value:{current_rec[flight.flight_number]}")
                                    break 

                # throttle test, 0 = no limit
                if config.dump_throttle() != 0 and line_counter == config.dump_throttle() :
                    break
        
        # all done wrap it up
        findings.add_finding(f"Rows checked {line_counter}")











    
    
    