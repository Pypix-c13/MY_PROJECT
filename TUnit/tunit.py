from pathlib import Path
import tomllib
import sys

def read_all_database_extension(database_folder = "database"):
    folder = Path(database_folder)
    kamus = {}
    
    if not folder.exists() and not folder.is_dir():
        print("Error: No such file or directory")
        return kamus
    
    for files in folder.glob("*.toml"):
        with open(files, "rb") as file:
            config = tomllib.load(file)

        source = str(config.get("source", ""))
        goto = str(config.get("goto", ""))
        
        if source:
            kamus[source] = goto
    return kamus

def main():
    if len(sys.argv) < 2:
        print("usage: python tunit.py [indonesian_source]")
        sys.exit(1)
    
    query = ''.join(sys.argv[1:]).strip().lower()
    kamus_data = read_all_database_extension()
    
    if query in kamus_data:
        print(kamus_data[query])
    else:
        print(f"kosakata '{query}' belum dipelajari")

if __name__ == "__main__":
    main()