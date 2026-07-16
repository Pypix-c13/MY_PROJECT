#!/bin/bash

mode="$1"
link="$2"
dest="$3"

mkdir -p "$dest"

if [ "$mode" == "--wget" ]; then
    wget -P "$dest" "$link"
elif [ "$mode" == "--git" ]; then
    if ! command -v git &> /dev/null; then
        echo "Error: Git not installed on your computer!"
        exit 1
    fi
    git clone "$link" "$dest"
else
    echo "Usage: $0 [--wget|--git] [link] [path]"
fi