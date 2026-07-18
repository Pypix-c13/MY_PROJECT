# APM - AutoPackageManager
software yang dibuat untuk membantu developer untuk melakukan file organize, compile, membuat project berbasis (C, Python dan Bash).

# Code Example
### File organize - All
```
bash organize.sh --all ~/Downloads
```
### File organize - Spesific
```
bash organize.sh --spesific [c|py|sh] ~/Downloads
```
### Scanning - All
```
bash scanning.sh --all ~/Downloads
```
### Scanning - Spesific
```
bash scanning.sh --spesific [c|py|sh] ~/Downloads
```
### Initialize Project
```
bash init.sh --initialize [c|py|sh] my_project
```
### Parsing - based on TOML
```
python targeted.py --compile init.toml
```
### Global Environment
```
bash global.sh
```
### Install dependencies
```
bash install.sh
```