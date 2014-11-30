from generator import generate
from generator import resolve

for i in xrange(1, 999999999):
    short = generate(i)
    if i == resolve(short):
        print("Pass: " , i)
    else:
        print("Error with: ", i)
