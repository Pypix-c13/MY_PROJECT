from pathlib import Path

def scanner():
    current_directory = Path('.')
    for items in current_directory.iterdir():
        if items.suffix == ".py":
            print(items.name)

scanner()