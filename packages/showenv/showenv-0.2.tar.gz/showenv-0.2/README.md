# Show Env

```shell script
                      __                 
    ____  __  _______/ /_  ____ _      __
   / __ \/ / / / ___/ __ \/ __ \ | /| / /
  / /_/ / /_/ (__  ) / / / /_/ / |/ |/ / 
 / .___/\__, /____/_/ /_/\____/|__/|__/  
/_/    /____/                            

```

É uma ferramenta para mostrar informações detalhadas de:
- Python
- Pip
- Libraries
- SO
- Disck usage

por projeto.

## Requirement
- Python 3.7 or more<br/>
- pip
- Python Virtual Environment (recomended)

## Install
```shell script
pip3 install showenv
```

## Running
```shell script
cd <REPOSITORY_TO_ANALYSE>
showenv
```


## Output
2 files generated in current project.


- config_environment.txt
```
OS:
Linux
Distributor ID:	Ubuntu
Description:	Ubuntu 19.04
Release:	19.04
Codename:	disco

Python Version:
Python 3.7.3

Pip Version:
pip 19.1.1 from $HOME/projetos/challenges/kaggle/porto-seguro-safe-driver-prediction/src/environment/venv/lib/python3.7/site-packages/pip (python 3.7)

Jupyter Version:
4.4.0

--------------------------------------------------

Disk Usage:

data:
383M	data/

virtual env:
736M	src/environment/venv/

all:
1,3G	.
```

- struture_project.txt
```
.
├── data
│   ├── kaggle_submission.csv
│   └── raw
│       ├── datasets.zip
│       ├── sample_submission.csv
│       ├── test.csv
│       └── train.csv
├── LICENSE
├── notebooks
│   └── porto_seguro_safe_driver.ipynb
├── README.md
├── references
│   └── porto-seguro-vector-logo.png
└── src
    └── environment
        ├── config_environment.txt
        ├── container
        │   └── Dockerfile
        ├── create_requirements.sh
        ├── create_virtual_env.sh
        ├── __init__.py
        ├── jupyter_notebook_config.py
        ├── makefile
        ├── prepare_env.py
        ├── README.md
        ├── requirements.txt
        ├── show_config_environment.sh
        ├── show_struture_project.sh
        ├── struture_project.txt
        ├── test_environment.py
        ├── venv
        └── virtualenv_requirements.txt

8 directories, 24 files
```
