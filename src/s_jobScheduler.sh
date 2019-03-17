#!/bin/bash

chmod +x *.R
chmod +x *.sh

# python s_run.py 0
# python s_run.py -0.1 &
# python s_run.py -0.2 &
# python s_run.py -0.5 &
# python s_run.py -0.75 &

python s_run_yule.py 0