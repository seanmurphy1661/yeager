import re

def generate_range_check(n,a,b):
    def __col_check(n):
        x = int(n)
        if x >= a and x <= b:
            return True
        else:
            return False 
    return __col_check 

def generate_required_check(n):
    def __required_check(n):
        if len(n) == 0 :
            return False
        else:
            return True
    return __required_check

def generate_regex_check(n,regex_string):
    p = re.compile(regex_string)
    def _regex_check(n):
        if p.match(n) == None:
            return False
        else:
            return True
    return _regex_check

def generate_regex_money_check(n):
    p = re.compile('/^-?\d+(,\d{3})*(\.\d{1,2})?$/')
    def _regex_money_check(n):
        if p.match(n) == None:
            return False
        else:
            return True
    return _regex_money_check



    
    