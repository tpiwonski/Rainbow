### Preparing Python environment
```
python3.6 -m venv env
source env/bin/activate
```

### Installing Python packages
```
pip install -r requirements.txt
```

### Usage
```
python main.py --pattern "\[API.+$" blue white underline --pattern "[0-9]{4}\-[0-9]{2}\-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}" green black crossout
```
