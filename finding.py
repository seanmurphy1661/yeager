class finding:
    """Handler for  findings"""

    def __init__(self,filename):
        """Initialize object"""
        self.filename = filename
        self.findings = []

    def add_finding(self,string):
        self.findings.append(string)

    def get_findings(self):
        return self.findings