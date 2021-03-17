#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: scriptShell.py
created time : 2021/03/16
last edit time : 2021/03/17
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

import datetime
from . import Script

context = """
#########################################################
## Model: {:<45}##
## Goal: Script for series of simulation               ##
## Author: Zhenyu Wei                                  ##
## Date: {:<46}##
#########################################################

# export PID={:<}
# while [ -e /proc/$PID ]
# do 
#     time=$(date "+%Y-%m-%d %H:%M:%S")
#     echo "$time: Process: $PID is still running"
#     sleep 300
# done
# time=$(date "+%Y-%m-%d %H:%M:%S")
# echo "$time: Start Simulation"

cd simulation 
python 01_min.py
python 02_heating_nvt.py
python 03_eq_npt.py
python 04_eq_nvt.py
python 05_sampling.py

# time=$(date "+%Y-%m-%d %H:%M:%S")
# echo "$time: End Simulation"
"""

class ScriptShell(Script):
    def __init__(
        self, save_dir: str, model_name: str, file_name='run.sh', parent_id=0
    ) -> None:
        super().__init__(save_dir, model_name, file_name)
        self.parent_id = parent_id
        
    def format_context(self):
        self.context = context.format(
            self.model_name, str(datetime.datetime.now().replace(microsecond=0)), 
            self.parent_id
        ) 