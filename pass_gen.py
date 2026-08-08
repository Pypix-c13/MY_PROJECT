import secrets
import string

def main(pw_length=12):
    letter = string.ascii_letters
    digit = string.digits
    special = string.punctuation
    
    all = letter + digit + special
    pwd = ''
    pw_strong = False
    
    while not pw_strong:
        pwd = ''
        
        for i in range(pw_length):
            pwd += ''.join(secrets.choice(all))
            
        if (any(char in special for char in pwd)) and (sum(char in digit for char in pwd) >= 2):
            pw_strong = True
    
    return pwd

if __name__ == "__main__":
    print(main())