import shutil, sys, pathlib, uuid
import os, tomllib, json, zipfile
import subprocess
from datetime import datetime

class Color:
    RED = "\033[31m"
    GREEN = "\033[92m"
    YELLOW = "\033[33m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    
class Message:
    def plain(text):
        print(text)
    def error(text):
        print(f"{Color.BOLD}{Color.RED}Error:{Color.RESET} {text}")
    def warning(text):
        print(f"{Color.BOLD}{Color.YELLOW}Warning:{Color.RESET} {text}")
    def success(text):
        print(f"{Color.BOLD}{Color.GREEN}Success:{Color.RESET} {text}")

class Check:
    def python():
        if not shutil.which("python") or not shutil.which("python3"):
            Message.error("Python/Python3 not found in your system!.")
            sys.exit(1)
        else:
            Message.success("Python/Python3 found in your system!.")
    def git():
        if not shutil.which("git"):
            Message.error("Git not found in your system!.\n")
            sys.exit(1)
        else:
            Message.success("Git found in your system!.\n")

class Command:    
    def help():
        print("usage: python3 vpack.py [options] [more]")
        print("options:")
        print("  help                               Show this help message")
        print("  link [toml_file_config]            Create a symbolic link")
        print("  zpack [--mcpack|--mcaddon] [input] Create mcpack or mcaddon archive")
        print("  commit [path] [repository_name]    Git auto-sync")
        print("  backup [project]                   Backup project to `backup` folder")
        print("  clean                              clear `backup` folder all\n")
    
    def link():
        if len(sys.argv) < 3:
            Message.error("No TOML config specified for `link`!")
            sys.exit(1)
        
        input_path = sys.argv[2]
        uuidgen = lambda: str(uuid.uuid4())
        
        if not pathlib.Path(f"{input_path}.toml").exists():
            Message.error(f"Config file {input_path}.toml not found!")
            sys.exit(1)
        
        with open(f"{input_path}.toml", "rb") as file:
            config = tomllib.load(file)
        
        header_config = config.get("header", {})
        header = {
            "allow_random_seed": bool(header_config.get("allow_random_seed", False)),
            "base_game_version": list(header_config.get("base_game_version", [1, 21, 0])),
            "description": str(header_config.get("des", "A Minecraft Addon")),
            "lock_template_options": bool(header_config.get("lock_template_options", False)),
            "name": str(header_config.get("name", "Unnamed Pack")),
            "min_engine_version": list(header_config.get("min_engine_version", [1, 20, 0])),
            "pack_scope": str(header_config.get("pack_scope", "any")),
            "version": list(header_config.get("version", [1, 0, 0])),
            "uuid": str(header_config.get("uuid", uuidgen()))
        }
        
        module_config = config.get("modules", {})
        modules = []
        
        if isinstance(module_config, dict) and module_config:
            module = {
                "description": str(module_config.get("des", "A Minecraft Add-on Modules")),
                "type": str(module_config.get("type", "")),
                "version": list(module_config.get("version", [1, 0, 0])),
                "uuid": str(module_config.get("uuid", uuidgen()))
            }
            
            if module["type"] == "script":
                module["entry"] = str(module_config.get("entry", "scripts/main.js"))
                module["language"] = str(module_config.get("language", "javascript"))
            
            modules.append(module)
        
        dependency_config = config.get("depen", {})
        dependencies = []
        
        if isinstance(dependency_config, dict) and dependency_config:
            dependency = {
                "module_name": str(dependency_config.get("module_name", "@minecraft/server")),
                "version": list(dependency_config.get("version", [1, 10, 0]))
            }
            dependencies.append(dependency)
        
        capabilities_config = config.get("cap", [])
        capabilities = []
        
        if isinstance(capabilities_config, list) and capabilities_config:
            for capability in capabilities_config:
                capabilities.append(str(capability))
        
        metadata_config = config.get("metadata", {})
        metadata = {
            "authors": list(metadata_config.get("authors", ["Unknown"])),
            "license": str(metadata_config.get("license", "MIT")),
            "url": str(metadata_config.get("url", "")),
            "product_type": "addon",
            "generated_with": metadata_config.get("generated_with", {})
        }
        
        manifest = {
            "format_version": 2,
            "header": header,
            "modules": modules,
            "dependencies": dependencies,
            "capabilities": capabilities,
            "metadata": metadata
        }
        
        if modules and modules[0].get("type") == "script":
            manifest["dependencies"] = dependencies
        if capabilities:
            manifest["capabilities"] = capabilities
        
        raw_path = config["location"].get("path")
        path_string = str(pathlib.Path(raw_path).resolve())
        
        full = os.path.join(path_string, str(header_config.get("name", "Unnamed Pack")))
        os.makedirs(full, exist_ok=True)
        manifest_path = os.path.join(full, "manifest.json")
        
        try:
            subprocess.run(['git', 'init'], cwd=full, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print(f"Git initialized successfully in {full}")
        except subprocess.CalledProcessError as e:
            Message.error(f"Failed to initialize git: {e.stderr.decode().strip()}")
        
        if modules and modules[0].get("type") == "script":
            scripts_path = os.path.join(full, "scripts")
            os.makedirs(scripts_path, exist_ok=True)
            
            main = os.path.join(scripts_path, "main.js")
            with open(main, "w", encoding="utf-8") as main_file:
                main_file.write("import { world } from '@minecraft/server';\n")
        
        if modules and modules[0].get("type") == "resources":
            resources_path = os.path.join(full, "textures")
            os.makedirs(resources_path, exist_ok=True)
        
        if modules and modules[0].get("type") == "data":
            data_path = os.path.join(full, "functions")
            os.makedirs(data_path, exist_ok=True)
            
            mcfunction = os.path.join(data_path, "main.mcfunction")
            with open(mcfunction, "w", encoding="utf-8") as mcfunction_file:
                mcfunction_file.write("say Hello, world!")
        
        target_folder = os.path.dirname(input_path)
        with open(manifest_path, "w", encoding="utf-8") as manifest_file:
            json.dump(manifest, manifest_file, indent=4)
        
        Message.success(f"Pack created successfully at {full}")

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
    
    def commit():
        if len(sys.argv) < 4:
            Message.error("No project specified for `commit`!", 4)
            sys.exit(1)
        Check.git()
        
        input_path = sys.argv[2]
        repo = sys.argv[3]
        
        if not pathlib.Path(".git").exists():
            subprocess.run("git init", shell=True)
            Message.success("Initialized a new Git Repository.")
        
        subprocess.run(["git", "add", input_path], check=True)
        subprocess.run(["git", "commit", "-m", "Update Repository"], check=True)
        
        subprocess.run(["git", "push", "origin", repo], check=True)
        Message.success(f"Changes committed and pushed to {repo} successfully.")
    
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

def main():
    if len(sys.argv) < 2:
        Message.error("No command specified! Use `help` for help.")
        sys.exit(1)
    arg = sys.argv[1]
    
    Check.python()
    Check.git()

    match arg:
        case "help":
            Command.help()
        case "link":
            Command.link()
        case "zpack":
            Command.zpack()
        case "commit":
            Command.commit()
        case "backup":
            Command.backup()
        case "clean":
            Command.clean()
        case _:
            Message.error(f"Unknown command: {arg}. Use `help` for help.")
            sys.exit(1)

if __name__ == "__main__":
    main()