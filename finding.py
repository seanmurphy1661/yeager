import datetime 

class finding:
    """Handler for  findings"""

    def __init__(self,filename):
        """Initialize object"""
        self.filename = filename
        self.findings = []
        self.add_finding(f"Object:{self.filename} created")

    def add_finding(self,string):
        self.findings.append([datetime.datetime.now(),string])

    def get_findings(self):
        return self.findings
    
    def dump_findings(self):
        print("Findings")
        print("-------------------")
        for wstr in self.findings:
            print(f"{wstr[0]} : {wstr[1]}")


