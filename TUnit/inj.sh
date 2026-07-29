file_name="$1"
indonesian_source="$2"
german_to="$3"

if [ ! -d "database" ]; then
    mkdir database
fi

touch database/"$file_name"
cat << EOF > database/"$file_name"
source = "$indonesian_source"
goto = "$german_to"
EOF