#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: manager.py
created time : 2021/03/20
last edit time : 2021/03/20
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

import time
import pandas as pd
import multiprocessing as mp

class Manager:
    def __init__(
        self, log_file: str, gpu_file: str, 
        target_dir, back_dir='',
        is_init_log=False, target_peptide_pair=None
    ) -> None:
        if not log_file.endswith('.csv'):
            raise ValueError('The log_file should be a .csv file')
        self.log_file = log_file
        self.gpu_file = gpu_file
        self.target_dir = target_dir
        self.back_dir = back_dir
        self.is_init_log = is_init_log
        if self.is_init_log:
            self.initLog()
        self.log = pd.read_csv(self.log_file)
        if target_peptide_pair != None:
            self.targets = self.log[[i in target_peptide_pair for i in list(self.log.loc[:, 'Peptide Pair'])]]
            self.targets = self.targets[self.targets['Status'] == 'Unfinished'] # Ignore finished target
        else:
            self.targets = self.log[self.log['Status'] == 'Unfinished']
        self.devices = []
        self.num_devices = 0

    def initGPULog(self):
        io = open(self.gpu_file, 'w')
        print('GPU Label', 'Status', 'Job', sep=',', file=io)
        for device in self.devices:
            print(device.label, 'Unoccupied', 'None', sep=',', file=io)
    
    def testDevices(self):
        if self.num_devices == 0:
            raise ValueError('The number of devices is 0')

    def addDevices(self, *devices):
        for device in devices:
            self.devices.append(device)
        self.num_devices = len(self.devices)
        self.initGPULog()

    def getUnoccupiedDevice(self):
        df = pd.read_csv(self.gpu_file)
        index = [i for i, j in enumerate(list(df['Status']=='Unoccupied')) if j == True]
        gpu_labels = list(df.loc[index, 'GPU Label'])
        res = []
        for device in self.devices:
            if device.label in gpu_labels:
                res.append(device)
        return res

    def startCalculation(self):
        self.testDevices()
        pool = mp.Pool(self.num_devices)        
        cur_pair = 0
        peptide_pairs = list(self.targets['Peptide Pair'])
        num_pairs = len(peptide_pairs)
        while cur_pair < num_pairs:
            if self.getUnoccupiedDevice() != []:
                for device in self.getUnoccupiedDevice():
                    if cur_pair >= num_pairs:
                        break
                    pool.apply_async(
                        self._targetFunc,
                        args=(device, peptide_pairs[cur_pair])
                    )
                    cur_pair += 1
                    time.sleep(5)
        pool.close()
        pool.join()