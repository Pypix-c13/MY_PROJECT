import sys
from pathlib import Path
import tomllib
import subprocess

def main():
    if len(sys.argv) < 3:
        print("Usage: script.py --compile <config.toml>")
        sys.exit(1)

    arg = sys.argv[1]
    
    if arg == "--compile":
        source_path = Path(sys.argv[2])
        
        # Validasi file
        if not source_path.exists():
            print(f"Error: {source_path} not found!")
            sys.exit(1)
        if source_path.suffix != ".toml":
            print(f"Error: file extension not support! {source_path}")
            sys.exit(1)
        if not source_path.is_file():
            print(f"Error: {source_path} isn't file!")
            sys.exit(1)
        
        try:
            with open(source_path, "rb") as file:
                config = tomllib.load(file)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        
        compiler = str(config.get("compiler", "none"))
        source_file = str(config.get("source", "none"))
        target_file = str(config.get("target", "none"))
        linked_file = str(config.get("linked", None))
        
        # Eksekusi berdasarkan compiler
        if compiler == "gcc":
            if linked_file:
                cmd = [compiler, linked_file, source_file, "-o", target_file]
            else:
                cmd = [compiler, source_file, "-o", target_file]
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print(f"Error: compilation failed with {compiler}")
        elif compiler in ["python", "python3"]:
            subprocess.run([compiler, source_file])
        elif compiler == "bash":
            subprocess.run([compiler, source_file])
        else:
            print(f"Error: unknown compiler! '{compiler}'.")
            sys.exit(1)

if __name__ == "__main__":
    main()