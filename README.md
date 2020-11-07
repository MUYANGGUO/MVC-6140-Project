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

---

## Structure:
```tree
.
├── MVC.py (wrapper)
├── Approx.py (approximate method module)
├── BnB.py (exact method module)
├── LS1.py (local search method 1 module)
├── LS2.py (local search method 2 module)
├── README.md
├── LICENSE
 - - - - - - -Output Folder  - - - - - - - 
├── outputs (outputs folder, for submission)
|   └── Solution Files
|   └── Solution Trace Files
└── report (report folder)
    └── ProjectDescription.pdf
    └── ProjectReport.pdf
 - - - - - - - - Data Input  - - - - - - - 
├── DATA (data folder, not submitted)
│   ├── ExampleSolutions
│   │   ├── dummy1.sol
│   │   ├── dummy2.sol
│   │   ├── email.sol
│   │   └── jazz.sol
│   ├── as-22july06.graph
│   ├── delaunay_n10.graph
│   ├── dummy1.graph
│   ├── dummy2.graph
│   ├── email.graph
│   ├── football.graph
│   ├── hep-th.graph
│   ├── jazz.graph
│   ├── karate.graph
│   ├── netscience.graph
│   ├── power.graph
│   ├── star.graph
│   └── star2.graph
 - - - - - - - - - - - - - - - - - - - -

```
