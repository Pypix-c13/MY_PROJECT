import sys, pathlib, shutil
import os, zipfile
from message import Message

def zpack():
    if len(sys.argv) < 4:
        sys.exit(1)
    choice = sys.argv[2]
    
    if choice == "--mcpack":
        input_path = sys.argv[3]
        if not pathlib.Path(input_path).exists() and not os.path.isdir(input_path):
            Message.error(f"Directory {input_path} is not a valid directory")
            sys.exit(1)
        
        shutil.make_archive(input_path, 'zip', root_dir=input_path, base_dir='.')
        os.rename(f"{input_path}.zip", f"{input_path}.mcpack")
        Message.success(f"Packaged successfully as {input_path}.mcpack")
    elif choice == "--mcaddon":
        if len(sys.argv) < 4:
            Message.error("No text file specified for `mcaddon`!")
            sys.exit(1)

        target_name = sys.argv[3]
        input_file = f"{target_name}.txt"
        path = pathlib.Path(input_file)

        if not path.exists() or not path.is_file():
            Message.error(f"File {input_file} not found or is not a valid file!")
            sys.exit(1)

        output_file = f"{target_name}.mcaddon"

        try:
            with open(input_file, "r", encoding="utf-8") as file:
                links = [line.strip() for line in file if line.strip()]
            with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipped:
                for i in links:
                    if not pathlib.Path(i).exists():
                        Message.error(f"File not found: {i}")
                        continue
                    zipped.write(i, arcname=os.path.basename(i))
            Message.success(f"Container successfully created as {output_file}")
        except Exception as e:
            Message.error(f"{str(e)}")
            sys.exit(1)