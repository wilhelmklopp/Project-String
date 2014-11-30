alphabet = ["", "b","c","d","f","g","h","j","k","m","n","p","q","r","s","t","v","w","x","y","z","B","C","D","F","G","H","J","K","M","N","P","Q","R","S","T","V","W","X","Y","3","4","5","6","7","8","9"]
def generate(iv):
    #iv = index value in database
    short = []
    final = ""
    for i in range(0, 7):
        short.append(alphabet[iv%len(alphabet)])
        iv = int(iv/len(alphabet))
        #print (iv) #testing
    for i in short:
        if i != "":
            final = final + i
    return (final)
def resolve(short):
    iv = 0
    #short is shortened URL
    short_array = []
    for i in short:
        short_array.append(i)
    for i in range(len(short_array)-1, -1, -1):
        iv = iv * len(alphabet) + alphabet.index(short_array[i])
    print (iv)
