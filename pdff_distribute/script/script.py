#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: script.py
created time : 2021/03/15
last edit time : 2021/03/17
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

import os

class Script:
    def __init__(self, save_dir: str, model_name: str, file_name: str) -> None:
        self.save_dir = save_dir
        self.model_name = model_name
        self.file_name = file_name

    def format_context(self):
        raise NotImplementedError('format_context has not been overloaded')

    def writeFile(self):
        self.format_context()
        f = open(os.path.join(self.save_dir, self.file_name), 'w')
        print(self.context, file=f)
        f.close()