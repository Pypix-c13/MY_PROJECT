import pathlib, shutil
from message import Message

def clean():
    backup_f = pathlib.Path("backup")
    while True:
        confirm = input("Are you sure you want to delete ALL backups? [y/n] ")
        if confirm == "y" or confirm == "Y":
            if backup_f.exists() and any(backup_f.iterdir()):
                for i in backup_f.iterdir():
                    if i.is_dir():
                        shutil.rmtree(i)
                    else:
                        i.unlink()
                        Message.success("All backup have been purged")
            else:
                Message.error("Backup folder is already empty or doesn't exist.")
            break
        elif confirm == "n" or confirm == "N":
            Message.plain("Operation cancelled..")
            break
        else:
            continue