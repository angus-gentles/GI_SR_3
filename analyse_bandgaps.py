#!/usr/bin/env python3

import numpy as np
import os
import re
import sys
import argparse
import h5py
from bandgap_qescf import qe_scf_bandgap_SR, qe_scf_lattice_param

def save_results_to_hdf5(xs, ys, base_dir, output_file="GI_SR_3.results.hdf5"):
    with h5py.File(output_file, "w") as h5f:
        for i in range(len(xs)):
            x = xs[i]
            y = ys[i]
            
            print(x,y)
            # Directory pattern
            dir_name = f"dir_In{x}Ga{1-x}As{1-y}Sb{y}_cube_3x3x3"
            dir_path = os.path.join(base_dir, dir_name)
            
            if not os.path.isdir(dir_path):
                print(f"Skipping missing directory: {dir_path}")
                continue

            bandgaps = []
            lattice_params = []

            # Loop over calc directories inside dir_path
            for subdir in sorted(os.listdir(dir_path)):
                subdir_path = os.path.join(dir_path, subdir)
                if not os.path.isdir(subdir_path) or not subdir.startswith("calc_"):
                    continue
                calc_num = subdir.split("_")[1]
                filename = f"In{x}Ga{1-x}As{1-y}Sb{y}_cube_3x3x3.{calc_num}.scf.out"
                filepath = os.path.join(subdir_path, filename)

                if not os.path.isfile(filepath):
                    print(f"Missing file: {filepath}")
                    continue

                try:
                    Eg = qe_scf_bandgap_SR(filepath)
                    a = qe_scf_lattice_param(filepath)
                    if isinstance(Eg, float):
                        bandgaps.append(Eg)
                    lattice_params.append(a)
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    continue

            if bandgaps:
                group_name = f"x_{x}_y_{y}"
                grp = h5f.create_group(group_name)
                grp.attrs["x"] = x
                grp.attrs["y"] = y
                if x==0.25 and y==1.0:
                    print(bandgaps)
                bands_ds=grp.create_dataset("Eg", data=bandgaps)
                bands_ds.attrs["mean"] = np.mean(bandgaps)
                bands_ds.attrs["std"] = np.std(bandgaps)
                bands_ds.attrs["var"] = np.var(bandgaps)
                lattice_ds=grp.create_dataset("a", data=lattice_params)
                lattice_ds.attrs["mean"] = np.mean(lattice_params)
                lattice_ds.attrs["std"] = np.std(lattice_params)
                bands_ds.attrs["var"] = np.var(bandgaps)
            else:
                print(f"No data for x={x}, y={y}")

# Example usage
xs = [0.0, 0.0,  0.0,   0.0, 0.0,   0.0,  0.0, 0.25, 0.375, 0.5, 0.625, 0.75, 1.0, 1.0,  1.0,   1.0, 1.0,   1.0,  1.0, 0.75, 0.625, 0.5, 0.375, 0.25]
ys = [0.0, 0.25, 0.375, 0.5, 0.625, 0.75, 1.0, 1.0,  1.0,   1.0, 1.0,   1.0,  1.0, 0.75, 0.625, 0.5, 0.375, 0.25, 0.0, 0.0,  0.0,   0.0, 0.0,   0.0]
base_dir = "."  # Or the full path to where your directories are

xs=[0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0]
ys=[0.0, 0.25, 0.5, 0.75, 1.0, 0.0, 0.25, 0.5, 0.75, 1.0]

save_results_to_hdf5(xs, ys, base_dir)
