from pathlib import Path
import sys
import os
import uuid
import json
import subprocess
import tomllib

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 targeted.py [TOML_config]\n")
        sys.exit(1)

    path = Path(sys.argv[1])
    uuidgen = lambda: str(uuid.uuid4())
    
    if not path.exists():
        print(f"Error: Config file {path} not found!\n")
        sys.exit(1)
    
    if Path(path).suffix != ".toml":
        print(f"Error: file {path} doesn't support TOML extension!\n")
        sys.exit(1)
    
    with open(path, "rb") as file:
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

    raw_path = config.get("location", {}).get("path")
    if not raw_path:
        print("Error: 'location.path' is required in the TOML config.\n")
        sys.exit(1)

    path_string = str(Path(raw_path).resolve())

    full = os.path.join(path_string, str(header_config.get("name", "Unnamed Pack")))
    os.makedirs(full, exist_ok=True)
    manifest_path = os.path.join(full, "manifest.json")

    try:
        subprocess.run(['git', 'init'], cwd=full, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"Git initialized successfully in {full}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to initialize git: {e.stderr.decode().strip()}")

    if modules and modules[0].get("type") == "script":
        scripts_path = os.path.join(full, "scripts")
        os.makedirs(scripts_path, exist_ok=True)
        
        main_script = os.path.join(scripts_path, "main.js")
        with open(main_script, "w", encoding="utf-8") as main_file:
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

    with open(manifest_path, "w", encoding="utf-8") as manifest_file:
        json.dump(manifest, manifest_file, indent=4)
    print(f"Pack created successfully at {full}")

if __name__ == "__main__":
    main()