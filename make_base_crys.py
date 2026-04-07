#!/usr/bin/env python3
import numpy as np
from yaml_class import yaml_proc

a=11.18111
a=1
base="In0.0Ga1.0As0.5Sb0.5_cube_3x3x3"
ab=yaml_proc(f"{base}.result.yaml",f"{base}.yaml")
ab.prepare_lattice(a)
#print(ab.arrangements[0])
#ab.to_crys("base.crys")
ab.to_xyz("test.xyz")
