from pathlib import Path

class AutoPackageManager:
    @staticmethod
    def scanner():
        current_directory = Path('.')
        for items in current_directory.iterdir():
            if items.suffix == ".py":
                print(items.name)

AutoPackageManager.scanner()