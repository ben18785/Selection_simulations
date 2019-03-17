#!/bin/bash

chmod +x *.R
chmod +x *.sh

# Moran
python s_run.py 0 &
python s_run.py -0.1 &
python s_run.py -0.2 &
python s_run.py -0.5 &
python s_run.py -0.75 &

# Yule
python s_run_yule.py 0 &
python s_run_yule.py -0.1 &
python s_run_yule.py -0.25 &
python s_run_yule.py -0.5 &
python s_run_yule.py -0.75 &