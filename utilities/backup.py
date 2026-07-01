import sys, pathlib, shutil, os
from datetime import datetime
from color import Color
from message import Message

def backup():
    if len(sys.argv) < 3:
        if not pathlib.Path("backup").exists():
            os.makedirs("backup", exist_ok=True)
            Message.success("`backup` folder has been created!")
            sys.exit(1)
        Message.error("No project specified for backup")
        sys.exit(1)
    
    input_path = pathlib.Path(sys.argv[2])
    backup_f = pathlib.Path("backup")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_folder = backup_f / timestamp
    
    target_folder.mkdir(parents=True, exist_ok=True)
    
    if input_path.is_dir():
        shutil.copytree(input_path, target_folder / input_path.name)
        Message.success(f"Backup folder {input_path} has been created!")
    elif input_path.is_file():
        shutil.copy2(input_path, target_folder / input_path.name)
        Message.success(f"Backup file {input_path} has been created!")