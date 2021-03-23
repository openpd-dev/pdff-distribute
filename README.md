# PDFF distribute: A distributed framework for calculation of PDFF

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Introduction

This repository stores the openmm input script for the calculation of PDFF. Meanwhile, this package provide a distributed calculation framework to utilized power of multi-gpu on multi serves efficiently.

## Demo

```python
import pdff_distribute as distribute

device0 = distribute.Device(
    hostname='xx.xxx.xxx.xxx', username='xxx', password='xxx',
    cuda_id=0, python_path='xxx',
    target_dir='xxx',
    back_dir='xxx'
)
device1 = distribute.Device(
    hostname='xx.xxx.xxx.xxx', username='xxx', password='xxx',
    cuda_id=1, python_path='xxx',
    target_dir='xxx',
    back_dir='xxx'
)
device2 = distribute.Device(
    hostname='xx.xxx.xxx.xxx', username='xxx', password='xxx',
    cuda_id=2, python_path='xxx',
    target_dir='xxx',
    back_dir='xxx'
)

manager = distribute.TorsionManager(
    log_file=os.path.join(cur_dir, 'test.csv'), gpu_file=os.path.join(cur_dir, 'gpu.csv'),
    target_dir=os.path.join(cur_dir, 'test_manager'), is_init_log=False
)
manager.startCalculation()
```