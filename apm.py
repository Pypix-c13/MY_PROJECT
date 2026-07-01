from pathlib import Path
import os

current_directory = Path('.')
for items in current_directory.iterdir():
    if items.suffix == ".py":
        clean = os.path.splitext(items.name)[0]
        print(clean)
