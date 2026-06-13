import binascii
import sys
import os

class COLOR:
    BLUE = '\033[38;2;79;193;255m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def converter(data):
    if os.path.exists(data):
        with open(data, 'r') as f:
            return "0x" + binascii.hexlify(f.read().encode('utf-8')).decode('utf-8')
    else:
        return "0x" + binascii.hexlify(data.encode('utf-8')).decode('utf-8')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{COLOR.BOLD}{COLOR.BLUE}# USAGE{COLOR.RESET}\npython3 my_hex.py [data]")
        print(f"{COLOR.BOLD}{COLOR.BLUE}# CONDITION{COLOR.RESET}\n- if [data] detects a file, the system will immediately convert the file's contents to hexadecimal.")
        print("- if [data] doesn't detect a file, the system will immediately output the hexadecimal code to the terminal.")
        sys.exit(1)
        
    binary = sys.argv[1]
    print(converter(binary))