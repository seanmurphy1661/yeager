
class flight:

    def __init__(self,flight_name,flight_number):
        self.flight_name = flight_name
        self.flight_number = flight_number
        self.flight_test_array = []

    def append_test(self,flight_test):
        self.flight_test_array.append(flight_test)
