#!/bin/bash

arg="$1"
lang="$2"
folder="$3"

if [[ -d "$folder" ]]; then
    cd "$folder" || exit
else
    echo "Direktory '$folder' not found!"
    exit 1
fi

if [[ "$arg" == "--spesific" ]]; then
    case "$lang" in
        "c")
            mkdir -p Clang && mv *.c Clang/ 2>/dev/null && echo "File .c has been moved!."
        ;;
        "py")
            mkdir -p Python && mv *.py Python/ 2>/dev/null && echo "File .py has been moved!."
        ;;
        "sh")
            mkdir -p Shell && mv *.sh Shell/ 2>/dev/null && echo "File .sh has been moved!."
        ;;
        *)
            echo "Language not support: $lang"
        ;;
    esac

elif [[ "$arg" == "--all" ]]; then
    mkdir -p Clang Python Shell

    ls *.c >/dev/null 2>&1 && mv *.c Clang/ && echo "Moving .c..."
    ls *.py >/dev/null 2>&1 && mv *.py Python/ && echo "Moving .py..."
    ls *.sh >/dev/null 2>&1 && mv *.sh Shell/ && echo "Moving .sh..."
    
    echo "Organize Finished!"
else
    echo "Argumen tidak valid. Gunakan --spesific atau --all"
fi