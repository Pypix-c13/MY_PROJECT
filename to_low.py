import os, sys, shutil

def process(data, mode):
    if not shutil.which("python") and not shutil.which("python3"):
        print("Python/Python3 not found! please install to use this tools!")
    content = open(data, 'r').read() if os.path.exists(data) else data

    if mode == "--hex":
        return "0x" + content.encode().hex()
    if mode == "--binary":
        return ' '.join(format(ord(c), '08b') for c in content)
    if mode == "--text":
        return ''.join(chr(int(b, 2)) for b in content.split())

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 to_low.py [--hex|--binary|--text] [data/file]")
        sys.exit(1)
    print(process(sys.argv[2], sys.argv[1]))
