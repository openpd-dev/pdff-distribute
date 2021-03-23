#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: torsionManager.py
created time : 2021/03/19
last edit time : 2021/03/19
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

import datetime, os
import pandas as pd
from . import Manager
from .. import TRIPLE_LETTER_ABBREVIATION
from .. import RecipeTorsion, Job, Device

class TorsionManager(Manager):
    def __init__(
        self, log_file: str, gpu_file: str, 
        target_dir, back_dir='',
        is_init_log=False, target_peptide_pair=None,
        model_name='PDFF Non-Bonded Potential'
    ) -> None:
        super().__init__(log_file, gpu_file, target_dir, back_dir=back_dir, is_init_log=is_init_log, target_peptide_pair=target_peptide_pair)
        self.model_name = model_name

    def initLog(self):
        io = open(self.log_file, 'w')
        print('Peptide Pair', 'Status', 'Device', 'Start', 'End', 'Elapsed', sep=',', file=io)
        num_peptides = len(TRIPLE_LETTER_ABBREVIATION)
        for i in range(num_peptides):
            for j in range(i, num_peptides):
                print(
                    TRIPLE_LETTER_ABBREVIATION[i]+'-'+TRIPLE_LETTER_ABBREVIATION[j],
                    'Unfinished', 'None', 'None', 'None', 'None', sep=',', file=io
                )
        io.close()

    def _targetFunc(self, device: Device, peptide_pair):
        df = pd.read_csv(self.gpu_file)
        index = list(df['GPU Label'] == device.label).index(True)
        df.loc[index, 'Status'] = 'Occupied'
        df.loc[index, 'Job'] = peptide_pair
        df.to_csv(self.gpu_file, index=False)
        os.system('clear')
        print(df, '\n')
        
        df = pd.read_csv(self.log_file)
        index = list(df['Peptide Pair'] == peptide_pair).index(True)
        df.loc[index, 'Device'] = device.label
        df.to_csv(self.log_file, index=False)
        
        peptide1, peptide2 = peptide_pair.split('-')
        recipe = RecipeTorsion(
            target_dir=self.target_dir, model_name=self.model_name,
            peptide1=peptide1, peptide2=peptide2, cuda_id=device.cuda_id
        )
        job = Job(recipe)
        
        start_time = datetime.datetime.now().replace(microsecond=0)
        df = pd.read_csv(self.log_file)
        index = list(df['Peptide Pair'] == peptide_pair).index(True)
        df.loc[index, 'Start'] = start_time
        df.to_csv(self.log_file, index=False)
        print(df)
        device.submitJob(job)
        
        df = pd.read_csv(self.gpu_file)
        index = list(df['GPU Label'] == device.label).index(True)
        df.loc[index, 'Status'] = 'Unoccupied'
        df.loc[index, 'Job'] = 'None'
        df.to_csv(self.gpu_file, index=False)
        os.system('clear')
        print(df, '\n')

        df = pd.read_csv(self.log_file)
        index = list(df['Peptide Pair'] == peptide_pair).index(True)
        end_time = datetime.datetime.now().replace(microsecond=0)
        df.loc[index, 'Status'] = 'Finished'
        df.loc[index, 'End'] = end_time
        df.loc[index, 'Elapsed'] = end_time - start_time
        df.to_csv(self.log_file, index=False)
        print(df)
    