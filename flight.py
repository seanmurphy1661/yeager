from check_factory import *

# required inputs:
#   file_to_test.column_list - provides the column name lookup for position
#   config.get_options - provides the list of requested tests
#   findings - in the odd case there are issuess we'd like know that
def build_flight_list(column_list,config_options,findings):
    flight_list = []
    column_number = 0
    for working_option in config_options:
        if "test" in working_option:
            #
            # Process test option
            #
            column_number = 0
            #
            #   name is required
            #
            if "name" not in working_option['test']:
                findings.add_finding("name tag required")
                next
            #
            #   use name to lookup column number, 
            #   all column references are by column_number
            #
            if working_option['test']['name'] in column_list:
                column_number = column_list.index(working_option['test']['name'])
            else:
                #
                # can't fly with out the number, reject test entry
                #
                print(f"column not found {working_option['test']['name']}:{column_list}")
                findings.add_finding(f"column not found {working_option['test']['name']}")
                next
            # column name and position in file are determined
            # create the flight object
            working_flight = flight(working_option['test']['name'], column_number)
            #
            # add regex flight test to the working flight
            #
            if 'regex' in working_option['test']:
                working_flight.append_flight_activity(flight_activity(
                    "regex test",
                    f"column failed regex test {working_option['test']['regex']}",
                    generate_regex_check("",working_option['test']['regex'])))
            #
            # add range flight activity to working flight
            #
            if 'range' in working_option['test']:
                working_flight.append_flight_activity(flight_activity(
                    "range test",
                    f"column failed range test {working_option['test']['range'][0]},{working_option['test']['range'][1]}",
                    generate_range_check(0,working_option['test']['range'][0],working_option['test']['range'][1])))
            #
            # add type flight activity to working flight
            # all flights start as string
            #
            if 'type' in working_option['test']:
                if working_option['test']['type'] == 'date':
                    working_flight.update_type("date")
                    working_flight.append_flight_activity(flight_activity(
                        "date type check",
                        "column failed date check",
                        generate_date_type_check("")))
                elif working_option['test']['type'] == 'number':
                    working_flight.update_type("number")
                    working_flight.append_flight_activity(flight_activity(
                        "number type check",
                        "column failed number check",
                        generate_number_type_check(0)
                    ))

        # all the flight tests are in, file the flight in the book
        flight_list.append(working_flight)
    return flight_list

#
#   class flight container for flight activities
#       flight_name - name for set of activities. atm this equals column name
#       flight_number - the column positional order
#       flight_type - a data type designation that enables other activivities
#       flight_activities - an array of flight activity objects
#
class flight:
    '''Models a flight. Flights have a column name, the number of the colum and a set of activities to preform on the column'''
    def __init__(self,flight_name,flight_number):
        self.flight_name = flight_name
        self.flight_number = flight_number
        self.flight_type = "string"
        self.flight_activities = []

    def update_type(self,flight_type):
        '''Used to validate and update flight type'''
        if flight_type in ["date","number","money"]:
            self.flight_type = flight_type
            return True
        return False

    def append_flight_activity(self,flight_activity):
        self.flight_activities.append(flight_activity)
#
#   flight activity contains 3 parts
#       name - name of activity requested (type, regex, and others)
#       message - message returned on activity failure
#       activity - a function that executes activity and returns result
#         see check_factory.py
#           true -> activity passed
#           false -> activity failed
#
#
class flight_activity:
    def __init__(self,name,message,activity):
        self.flight_activity_name = name
        self.flight_activity_message = message
        self.flight_activity = activity

   