generate(iv):
    #iv = index value in database
    alphabet = ["b","c","d","f","g","h","j","k","m","n","p","q","r","s","t","v","w","x","y","z","B","C","D","F","G","H","J","K","M","N","P","Q","R","S","T","V","W","X","Y","3","4","5","6","7","8","9"]
    short = []
    short.append(alphabet[iv%len(alphabet)])
    print (short)
