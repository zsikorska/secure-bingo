# sec-bingo
unit course: organisational and informational security - project 2

# Authors
 - 112169 MIRON ARTUR OSKROBA
 - 112018 ZUZANNA SIKORSKA
 - 112282 JANNIS JAKOB MALENDE
 - 112059 STANISLAW FRANCZYK
 
# How to run all-in-one simulation
0. Clone repo `git clone https://github.com/detiuaveiro/sec-bingo.git` and `cd sec-bingo`
1. set PYTHONPATH from `sec-bingo` directory
```
export PYTHONPATH=$PWD
echo $PYTHONPATH
```

2. Run the Broker. From the `sec-bingo` directory, execute
```
make up
```
3. Prepare Python environment
```
python3 -m venv ./venv
```
4. Activate python3 virtual environment (venv):
```
source ./venv/bin/activate
```
5. install python modules requirements:
```
pip3 install -r requirements.txt
```
6. Run PoC using configured venv
```
python3 client_simulator/client_simulator.py
```

### Python development tips for MacOS|Linux
1. Create venv.
```
python3 -m venv ./venv
```
2. Activate python3 virtual environment (venv):
```
source ./venv/bin/activate
```
3.  install python modules requirements:
```
pip3 install -r requirements.txt
```
3. At this point `python3` binary should be ready. `which python3`
