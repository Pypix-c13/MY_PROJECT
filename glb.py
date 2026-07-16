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
    files = Path(sys.argv[1])
    if files.suffix != ".toml":
        print(f"Error: File {files} doesn't support TOML extension!.\n")
        sys.exit(1)
    if not files.exists() and not files.is_file():
        print("Error: No such file or directory!.\n")
        sys.exit(1)

    with open(files, "rb") as file:
        config = tomllib.load(file)

    alias_name = config.get("alias_name")
    command = config.get("command")

    if not alias_name or not command:
        print("Error: alias_name and command must be set in the TOML file.\n")
        sys.exit(1)

    append_alias_to_bashrc(alias_name, command)
    print(f"Added alias '{alias_name}' to {Path.home() / '.bashrc'}")


if __name__ == "__main__":
    main()
