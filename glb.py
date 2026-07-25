import sys
from pathlib import Path
import tomllib
from shlex import quote as shell_quote


def append_alias_to_bashrc(alias_name, command):
    bashrc_path = Path.home() / ".bashrc"
    alias_line = f"alias {alias_name}={shell_quote(command)}\n"

    if bashrc_path.exists():
        existing = bashrc_path.read_text(encoding="utf-8")
    else:
        existing = ""

    if alias_line.strip() in existing.splitlines():
        print(f"Alias '{alias_name}' already exists in {bashrc_path}.")
        return

    with bashrc_path.open("a", encoding="utf-8") as file:
        if existing and not existing.endswith("\n"):
            file.write("\n")
        file.write(alias_line)

def main():
    if len(sys.argv) < 3:
        print("usage: python glb.py [alias_name: str] [command: str]")
        sys.exit(1)
    
    alias_name = sys.argv[1]
    command = sys.argv[2]
    append_alias_to_bashrc(alias_name=alias_name, command=command)

if __name__ == "__main__":
    main()