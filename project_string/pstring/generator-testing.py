# tests validity of each generated short
from generator import generate
from generator import resolve

for i in xrange(10000000, 999999999):
    short = generate(i)
    if i == resolve(short):
        print("Pass: " , i, short)
    else:
        print("Error with: ", i, short, "--------")
#tested up to 10 million
