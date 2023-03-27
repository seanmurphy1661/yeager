from check_factory import generate_range_check
from check_factory import generate_required_check

n = 15
m = 20 

 
test_list = {
    'range': generate_range_check(n,10,20),
    'required': generate_required_check(n)
}

z = generate_range_check(n,10,20)
x = generate_required_check(n)

print(f"Range check {test_list['range'](40)}")
print(f"Data Present: {x('')}")
print (z)