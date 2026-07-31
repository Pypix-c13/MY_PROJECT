from deep_translator import GoogleTranslator
import sys

def _translate_():
    if len(sys.argv) < 3:
        print("usage: python ig.py [--to-indonesian | --to-german] [word]")
        sys.exit(1)
    
    if sys.argv[1] == "--to-indonesian":
        translated = GoogleTranslator(source='de', target='id').translate(sys.argv[2])
        print(translated)
    elif sys.argv[1] == "--to-german":
        translated_ = GoogleTranslator(source='id', target='de').translate(sys.argv[2])
        print(translated_)

if __name__ == "__main__":
    _translate_()