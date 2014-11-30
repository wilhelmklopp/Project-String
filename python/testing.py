from generator import generate
from generator import resolve

for i in xrange(53833, 999999999):
    short = generate(i)
    if i == resolve(short):
        print("Pass: " , i, short)
    else:
        print("Error with: ", i, short)
