def help():
    print("usage: python3 vpack.py [options] [more]")
    print("options:")
    print("  help                               Show this help message")
    print("  link [toml_file_config]            Create a symbolic link")
    print("  zpack [--mcpack|--mcaddon] [input] Create mcpack or mcaddon archive")
    print("  commit [path] [repository_name]    Git auto-sync")
    print("  backup [project]                   Backup project to `backup` folder")
    print("  clean                              clear `backup` folder all\n")