#!/bin/bash

# Argumen
arg="$1"
lang="$2"
path="$3"

if [[ -z "$path" ]]; then
    echo "Usage: $0 --initialize [c|py|sh] [folder_name]"
    exit 1
fi

if [[ "$arg" == "--initialize" ]]; then
    case "$lang" in
        c)
            mkdir -p "$path" && cd "$path" || exit
            touch main.c init.toml
            cat <<EOF > init.toml
compiler = "gcc"
source = "main.c"
target = "main"
linked = "-Wall"
EOF
            echo "Project C initialized at $path"
            ;;
        py)
            mkdir -p "$path" && cd "$path" || exit
            touch main.py init.conf
            cat <<EOF > init.toml
compiler = "python3"
source = "main.py"
EOF
            echo "Project Python initialized at $path"
            ;;
        sh)
            mkdir -p "$path" && cd "$path" || exit
            touch main.sh init.toml
            cat << EOF > init.toml
compiler = "bash"
source = "main.sh"
EOF
            echo "Project Shell initialized at $path"
            ;;
        *)
            echo "Error: Language must be [c, py, sh]"
            exit 1
            ;;
    esac
else
    echo "Command not recognized. Use --initialize."
fi