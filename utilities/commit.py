import sys, subprocess, pathlib
from message import Message
import shutil

def commit():
    if len(sys.argv) < 4:
        Message.error("No project specified for `commit`!", 4)
        sys.exit(1)
    if not shutil.which("git"):
        Message.error("Git not found in your system!.\n")
        sys.exit(1)
    else:
        Message.success("Git found in your system!.\n")
    
    input_path = sys.argv[2]
    repo = sys.argv[3]
    
    if not pathlib.Path(".git").exists():
        subprocess.run("git init", shell=True)
        Message.success("Initialized a new Git Repository.")
    
    subprocess.run(["git", "add", input_path], check=True)
    subprocess.run(["git", "commit", "-m", "Update Repository"], check=True)
    
    subprocess.run(["git", "push", "origin", repo], check=True)
    Message.success(f"Changes committed and pushed to {repo} successfully.")