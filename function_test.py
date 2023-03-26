from check_factory import generate_range_check
from check_factory import generate_required_check

n = 15
m = 20 


test_list = [generate_range_check(n,10,20),generate_required_check(n)]

z = generate_range_check(n,10,20)
x = generate_required_check(n)

l = z(m)

print(l)

print(f"Range check {test_list[0](40)}")
print(f"Data Present: {x('')}")
print (z)