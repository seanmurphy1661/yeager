

class flight:
    '''Models a flight. Flights have a column name, the number of the colum and a set of activities to preform on the column'''
    def __init__(self,flight_name,flight_number):
        self.flight_name = flight_name
        self.flight_number = flight_number
        self.flight_activities = []

    def append_flight_activity(self,flight_activity):
        self.flight_activities.append(flight_activity)

class flight_activity:
    def __init__(self,name,message,activity):
        self.flight_activity_name = name
        self.flight_activity_message = message
        self.flight_activity = activity

   