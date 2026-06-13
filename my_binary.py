import sys
import os

def to_binary(data):
	if os.path.exists(data):
		with open(data, 'r') as f:
			return ' '.join(format(ord(i), '08b') for i in f.read())
	else:
		return ' '.join(format(ord(j), '08b') for j in data)

def to_text(data):
	if os.path.exists(data):
		with open(data, 'r') as file:
			return ' '.join(chr(int(b, 2)) for b in data.split())
	else:
		return ''.join(chr(int(k, 2)) for k in data.split())

def page():
	if len(sys.argv) < 3:
		print("NO ARGUMENTS!")
		sys.exit(1)

	flags = sys.argv[1]
	data = sys.argv[2]

	if flags == "--binary":
		print(to_binary(data))
	elif flags == "--text":
		print(to_text(data))
	else:
		print("must be --binary or --text")

page()
