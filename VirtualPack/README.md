# VPACK - VirtualPack
sebuah software yang diciptakan untuk memudahkan seorang developer dalam membuat structure folder dan manifest.json
mendukung TOML configuration file yang memudahkan siapa saja untuk menulis manifest.json tanpa membuat jari kelelahan berlebih.

# Example code
### Make new Project
```
bash vpack.sh --template [data|script|resource] my_project ~/Downloads
```
### Packages
```
bash vpack.sh --package [--mcpack|--mcaddon] ~/Downloads/my_project
```
### Parsing TOML configuration
```
python targeted.py ~/Downloads/my_project/init.toml
```
### Global env
```
bash global.sh
```
