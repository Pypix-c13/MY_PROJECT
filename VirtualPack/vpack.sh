#!/bin/bash

# --template [data|resource|script] [name] [target_path]
# --package [--mcpack|--mcaddon] [target_path]

arg="$1"

if [[ "$arg" == "--template" ]]; then
    type_of="$2"
    name="$3"
    target_path="${4:-.}"
    full_path="$target_path/$name"

    if [[ -z "$type_of" || -z "$name" ]]; then
        echo "Usage: $0 --template [data|resource|script] [name] [target_path]"
        exit 1
    fi

    case "$type_of" in
        data)
            module_type="data"
            ;;
        script)
            module_type="script"
            ;;
        resource)
            module_type="resources"
            ;;
        *)
            echo "Error: Unknown template type '$type_of'. Use data, resource, or script."
            exit 1
            ;;
    esac

    mkdir -p "$full_path"

    cat << EOF > "$full_path/init.toml"
[header]

[modules]
type = "$module_type"

[metadata]

[location]
path = "$full_path"
EOF

    echo "Project $name created at $full_path"

elif [[ "$arg" == "--package" ]]; then
    pkg_type="$2"
    folder="$3"

    if [[ ! -d "$folder" ]]; then
        echo "Error: Folder $folder not found!"
        exit 1
    fi

    ext=""
    [[ "$pkg_type" == "--mcpack" ]] && ext="mcpack"
    [[ "$pkg_type" == "--mcaddon" ]] && ext="mcaddon"

    if [[ -n "$ext" ]]; then
        zip -r "${folder}.${ext}" "$folder"
        echo "Package created: ${folder}.${ext}"
    else
        echo "Error: Unknown package type"
    fi
fi
