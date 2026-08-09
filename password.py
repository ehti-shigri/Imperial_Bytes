import random
pass1=(input("Enter a group of numbers: "))
pass2=(input("Enter a group of letters: "))
pass3=(input("Enter a group of special characters: "))
#password ={pass1, pass2, pass3}

password={
 random.choice(pass1),
 random.choice(pass2),
    random.choice(pass3)
} # this will pick a character from eachgroup 
 
password2=random.choices(pass1+pass2+pass3, k=5) # pick 5 random char

password2.extend(password)

print("your password is :", password2) #list type print

print ("your password is:" + " ".join(password2)) #string type print