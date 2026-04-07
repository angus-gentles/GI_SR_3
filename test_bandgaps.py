#!/usr/bin/env python3

import numpy as np
import os
import re
import sys
import argparse
import h5py
from bandgap_qescf import qe_scf_bandgap_SR, qe_scf_lattice_param

base="In1.0Ga0.0As0.5Sb0.5"
base1=f"{base}_cube_3x3x3"
Egs=[]
for i in range(10):
    try:
        Eg=float(qe_scf_bandgap_SR(f"dir_{base1}/calc_{i}/{base1}.{i}.scf.out"))
        Egs.append(Eg)
    except:
        continue

print(f"Mean Eg={np.mean(Egs):.4f} eV")
print(f"Std  Eg={np.std(Egs):.4f} eV")
