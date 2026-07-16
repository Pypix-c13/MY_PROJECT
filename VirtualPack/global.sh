#!/bin/bash

BASHRC="$HOME/.bashrc"
VPACK_DIR="$HOME/VirtualPack"

ALIASES=(
    "alias vpack-init='$VPACK_DIR/vpack.sh'"
    "alias vpack-targeted='$VPACK_DIR/targeted.py'"
)

FILES=(
    "$VPACK_DIR/vpack.sh"
    "$VPACK_DIR/targeted.py"
)

echo "Checking VPACK files..."

for file in "${FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "Error: File not found! -> $file"
        exit 1
    fi
done

echo "Updating .bashrc configuration..."

# Menambahkan header jika belum ada
if ! grep -q "# VPACK Configuration" "$BASHRC"; then
    echo -e "\n# VPACK Configuration" >> "$BASHRC"
fi

for entry in "${ALIASES[@]}"; do
    if ! grep -qF "$entry" "$BASHRC"; then
        echo "$entry" >> "$BASHRC"
        echo "Added: $entry"
    else
        echo "Exists: $entry"
    fi
done

echo "Finished! Run 'source ~/.bashrc' to apply changes."