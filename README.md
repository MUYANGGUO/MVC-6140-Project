# MVC-6140-Project
CSE-6140 Project - Minimum Vertex Cover

---

MVC.py is the wrapper script for running the experiements. It handles input, outputs. 

## MAN page:
```bash
python3 MVC.py -h
```

```
usage: MVC.py [-h] filename {BnB,Approx,LS1,LS2} time seed

positional arguments:
  filename              name of the data file
  {BnB,Approx,LS1,LS2}  alg method to use
  time                  cut-off time in seconds
  seed                  random seed applicable to randomized methods only

optional arguments:
  -h, --help            show this help message and exit
```

## Example:

```zsh
python3 MVC.py './DATA/football.graph' 'BnB' 2.0 1  
```
