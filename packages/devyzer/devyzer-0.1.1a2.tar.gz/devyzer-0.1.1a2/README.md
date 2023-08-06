## Installation

- prepare  virtual environment 
- install requirements
```
pip install -r requirements.txt
```


## Run Package

login:

```
 python  -m devyzer_cli.main -L

```
or
```
 python  -m devyzer_cli.main --login

```


talk:

```
  python  -m devyzer_cli.main
    
```

help:

```
  python  -m devyzer_cli.main --help

```
sudo apt-get install alien
python setup.py bdist --formats=rpm
cd dist/
sudo alien devyzer-0.1.0-1.noarch.rpm
sudo dpkg -i devyzer_0.1.0-2_all.deb
sudo dpkg --remove devyzer
