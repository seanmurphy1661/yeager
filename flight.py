
class flight:

    def __init__(self,name):
        self._flight_name = name
        self._flight_test = []

    def append_test(self,flight_test):
        self._flight_test.append(flight_test)
