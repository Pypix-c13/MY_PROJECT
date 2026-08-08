trash="$HOME/.local/share/Trash"
cache="$HOME/.cache"
config="$HOME/.config"
tmp="/tmp"

if [ -z "$(ls -A "$trash" 2>/dev/null)" ] && [ -z "$(ls -A "$cache" 2>/dev/null)" ] && [ -z "$(ls -A "$config" 2>/dev/null)" ] && [ -z "$(ls -A "$tmp" 2>/dev/null)" ]; then
    echo "file not found!"
else
    sudo rm -rf "$trash"/* "$cache"/* "$config"/* "$tmp"/*
    echo "file has been deleted!"
fi
