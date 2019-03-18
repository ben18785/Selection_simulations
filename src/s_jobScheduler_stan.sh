#!/bin/bash

chmod +x *.R
chmod +x *.sh

run_selection()
{
  selection=$1
  for i in {2..15}
  do
   Rscript s_run_stan.R $selection $i
  done
}

for s in 0.00 -0.10 -0.25 -0.50 -0.75 -1.00
do
 run_selection $s
done