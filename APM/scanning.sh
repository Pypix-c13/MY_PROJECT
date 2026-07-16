#!/bin/bash

arg="$1"

if [[ "$arg" == "--spesific" ]]; then
    lang="$2"
    directory="$3"
    if [[ -d "$directory" ]]; then
        cd "$directory" || exit
        case "$lang" in
            c)  ls -a | grep "\.c$" ;;
            py) ls -a | grep "\.py$" ;;
            sh) ls -a | grep "\.sh$" ;;
            *)  echo "Error: Language not supported! $lang" ;;
        esac
    else
        echo "Directory '$directory' not found!"
    fi

elif [[ "$arg" == "--all" ]]; then
    path="$2"
    if [[ -d "$path" ]]; then
        cd "$path" || exit
    else
        echo "Directory '$path' not found!"
        exit 1
    fi

    echo "================"
    echo "   C Languages  "
    echo "================"
    ls -a | grep "\.c$"
    echo "================"
    echo -e "\n"

    echo "================"
    echo "Python Languages"
    echo "================"
    ls -a | grep "\.py$"
    echo "================"
    echo -e "\n"

    echo "================"
    echo " Shell Scripts  "
    echo "================"
    ls -a | grep "\.sh$"
    echo "================"
fi