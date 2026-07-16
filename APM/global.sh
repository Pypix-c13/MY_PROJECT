#!/bin/bash

BASHRC="$HOME/.bashrc"
APM_DIR="$HOME/APM"

ALIASES=(
    "alias apm-init='$APM_DIR/init.sh'"
    "alias apm-scanning='$APM_DIR/scanning.sh'"
    "alias apm-organize='$APM_DIR/organize.sh'"
    "alias apm-targeted='$APM_DIR/targeted.py'"
    "alias apm-install='$APM_DIR/install.sh'"
)

FILES=(
    "$APM_DIR/init.sh"
    "$APM_DIR/scanning.sh"
    "$APM_DIR/organize.sh"
    "$APM_DIR/targeted.py"
    "$APM_DIR/install.sh"
)

echo "Check file APM..."

for file in "${FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "Error: File not found! -> $file"
        exit 1
    fi
done

echo "Added configuration to .bashrc..."
echo -e "\n# APM Configuration" >> "$BASHRC"

for entry in "${ALIASES[@]}"; do
    if ! grep -qF "$entry" "$BASHRC"; then
        echo "$entry" >> "$BASHRC"
    else
        echo "Exists: $entry"
    fi
done

echo "Finished! Run 'source ~/.bashrc for see change!'."
