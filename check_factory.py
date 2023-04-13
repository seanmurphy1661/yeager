import re
from dateutil.parser import parse 
#
#   generate_range_check(n,a,b) - col between min / max
#   generate_required_check(n) - 0 len string
#   generate_regex_check(n,regex_string) - any valid regex
#   generate_regex_money_check(n) - money format 
#   generate_number_type_check(n) - number data type
#   generate_date_type_check(n) - date data type
# -------------------------------------------------------------------------
#
#   returns a function that will compare the value
#   to a specified range 
#   column must be an integer
#
def generate_range_check(n,a,b):
    def _range_check(n):
        x = int(n)
        if x >= a and x <= b:
            return True
        else:
            return False 
    return _range_check 
#
#   returns a function that tests for 0 len column
#   True = 1+ characters
#   False = 0 len string
#
def generate_required_check(n):
    def __required_check(n):
        if len(n) == 0 :
            return False
        else:
            return True
    return __required_check
#
#   generic regex test
#   True = column matches expression
#   False = no match
#
def generate_regex_check(n,regex_string):
    p = re.compile(regex_string)
    def _regex_check(n):
        if p.match(n) == None:
            return False
        else:
            return True
    return _regex_check
#
#   type money check using regex
#       2 decimal limit
#   True = column matches expression
#   False = no match
#
def generate_regex_money_check(n):
    p = re.compile('/^-?\d+(,\d{3})*(\.\d{1,2})?$/')
    def _regex_money_check(n):
        if p.match(n) == None:
            return False
        else:
            return True
    return _regex_money_check
#
#   type number check using regex
#   True = column matches expression
#   False = no match
#
def generate_number_type_check(n):
    p = re.compile("^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$")
    def _number_check(n):
        if p.match(n) == None:
            return False
        else:
            return True
    return _number_check
#
#   type date check using dateutil.parse
#   True = column can be parsed to a date column
#   False = not a date string
#
def generate_date_type_check(n):
    def _date_check(n):
        try:
            parse(n)
            return True
        except:
            return False
    return _date_check
    
    