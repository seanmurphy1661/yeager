
def generate_range_check(n,a,b):
    def __col_check(n):
        if n >= a and n <= b:
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
    
    