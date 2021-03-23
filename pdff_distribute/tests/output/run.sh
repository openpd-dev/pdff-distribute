
#########################################################
## Model: alpha helix validation                       ##
## Goal: Script for series of simulation               ##
## Author: Zhenyu Wei                                  ##
## Date: 2021-03-19 20:47:31                           ##
#########################################################

# export PID=0
# while [ -e /proc/$PID ]
# do 
#     time=$(date "+%Y-%m-%d %H:%M:%S")
#     echo "$time: Process: $PID is still running"
#     sleep 300
# done
# time=$(date "+%Y-%m-%d %H:%M:%S")
# echo "$time: Start Simulation"

cd simulation 
$python 01_min.py
$python 02_heating_nvt.py
$python 03_eq_npt.py
$python 04_eq_nvt.py
$python 05_sampling.py

# time=$(date "+%Y-%m-%d %H:%M:%S")
# echo "$time: End Simulation"

