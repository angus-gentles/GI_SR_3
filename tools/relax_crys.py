#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 14:29:39 2024

@author: gentles
"""

import re
import numpy as np
import argparse

def extract_atomic_positions(output_file):
    print(output_file)
    p1=re.compile(r"(\S+)\s+tau\(\s+1\)\s+=\s+\(\s+(\S+)\s+(\S+)\s+(\S+)\s+\)")
    with open(output_file, 'r') as f:
        line = 'her'
        line=line.strip()
        reading_coords = False
        all_coordinates=[]
        switch1=True
        first_coordinates=[]
        while line:
            #atom_info = line.strip().split()
            line=line.strip()
            if switch1==True:
                q1=p1.search(line)
                if q1:
                    first_coordinates.append([q1.group(1),q1.group(2),q1.group(3),q1.group(4)])
            if 'Estimated max dynamical RAM per process' in line and switch1==True:
                switch1=False
                print('first_coords len:',len(first_coordinates))
                all_coordinates.append(first_coordinates)
            if 'ATOMIC_POSITIONS' in line:
                current_coord=[]
                reading_coords = True
            elif reading_coords and (len(line)==0 or "End final coordinates" in line):
                reading_coords = False
                all_coordinates.append(current_coord)
            elif reading_coords and len(line)!=0:
                atom_info = line.split()
                current_coord.append(atom_info)
            line = f.readline()
    return all_coordinates

        

def extract_lattices(output_file):
    p1=re.compile(r'CELL_PARAMETERS \(alat= ([0-9|\.]+)\)')
    p2=re.compile(r"celldm\(1\)=\s+(\S+)")
    p3=re.compile(r"a\([0-9]\)\s+=\s+\(\s+(\S+)\s+(\S+)\s+(\S+)\s+\)")
    with open(output_file, 'r') as f:
        line = 'her'
        line=line.strip()
        reading_coords = False
        all_coordinates=[]
        alats=[]
        switch1=True
        first_lat=[]
        while line:
            #atom_info = line.strip().split()
            line=line.strip()
            if switch1==True:
                q2=p2.search(line)
                q3=p3.search(line)
                if 'Estimated total dynamical RAM' in line:
                    switch1=False
                    #first_lat=np.array(first_lat)
                    all_coordinates.append(first_lat)
                elif q2:
                    alats.append(float(q2.group(1)))
                elif q3:
                    first_lat.append([q3.group(1),q3.group(2),q3.group(3)])
                else:
                    pass
            else:
                pass
            if 'CELL_PARAMETERS' in line:
                q1=p1.search(line)
                if q1:
                    alat=q1.group(1)
                    alats.append(float(alat))
                current_coord=[]
                reading_coords = True
            elif reading_coords and len(line)!=0:
                atom_info = line.split()
                current_coord.append(atom_info)
            elif reading_coords and len(line)==0:
                reading_coords = False
                all_coordinates.append(current_coord)
            line = f.readline()
        alats=np.array(alats,dtype=float)
    return all_coordinates,alat,alats

def extract_energies(output_file):
    p1=re.compile(r"!\s+total energy\s+=\s+(\S+) Ry")
    with open(output_file, 'r') as fi:
        line='her'
        all_energies=[]
        while line:
            line=line.strip()
            q1=p1.search(line)
            if q1:
                all_energies.append(float(q1.group(1)))
            line=fi.readline()
    return np.array(all_energies)

def main():
    parser = argparse.ArgumentParser(description='params')
    parser.add_argument('-x', dest='x', type=float, default=0.5)
    parser.add_argument('-y', dest='y', type=float, default=0.0)
    parser.add_argument('-N', dest='N', type=int,nargs=3, default=(3,3,3))
    parser.add_argument('--relaxout', dest='relax_out', type=str, default='none')
    parser.add_argument('--crysout', dest='crys_out', type=str, default='none')
    args = parser.parse_args()

    x=args.x
    y=args.y
    N=args.N

    x=round(x,2)
    y=round(y,2)
    x1=round(1-x,2)
    y1=round(1-y,2)



    crys_out=args.crys_out
    relax_out=args.relax_out
    base="In%sGa%sAs%sSb%s_%sx%sx%s"%(x,x1,y1,y,N[0],N[1],N[2])
    if relax_out=='none':
        relax_out="%s.relax.out"%base
    if crys_out=='none':
        crys_out='%s.out.crys'%base

    #output_file='./%s.relax.out'%base
    all_coordinates = extract_atomic_positions(relax_out)
    lattice,alat,alats=extract_lattices(relax_out)
    alat=float(alat)
    with open(relax_out) as fi:
        s1=fi.read()
    q1=re.compile(r"bravais-lattice index\s+=\s+([0-9]+)").search(s1)
    if q1:
        ibrav=int(q1.group(1))
    energies=extract_energies(relax_out)
    lowest_int=np.where(energies==energies.min())[0][0]
    print('the lowest interger is %s'%(lowest_int))
    print('length of energies: %s, length of coordinates: %s, length of lattices: %s, length of alats: %s'%(len(energies),len(all_coordinates),len(lattice),len(alats)))

    last_step=all_coordinates[lowest_int]
    last_lattice=lattice[lowest_int]
    if ibrav==2:
        alat_new=np.abs(alat*float(last_lattice[0][0])*2)
    elif ibrav==1:
        alat_new=np.abs(alat*float(last_lattice[0][0]))
    comment='alat=%s'%alat_new
    s="%s\n%s\n"%(len(last_step),comment)
    for line in last_step:
        s+="%s %s %s %s\n"%tuple(line)

    with open(crys_out,'w') as fo:
        fo.write(s)
        fo.close()
if __name__ == "__main__":
    main()