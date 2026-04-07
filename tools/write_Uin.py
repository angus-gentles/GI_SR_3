#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 13:24:35 2024

@author: aget
"""

import json
import numpy as np
import argparse

def write_Uin(x,y,U_base_file,U_out_file):
    
    with open(U_base_file,'r') as ui:
        U_params=json.load(ui)
        
    
    U_in={}
    U_in['In-5p']=y*U_params['InSb']['In-5p']+(1-y)*U_params['InAs']['In-5p']
    U_in['Ga-4p']=y*U_params['GaSb']['Ga-4p']+(1-y)*U_params['GaAs']['Ga-4p']
    U_in['As-4p']=x*U_params['InAs']['As-4p']+(1-x)*U_params['GaAs']['As-4p']
    U_in['Sb-5p']=x*U_params['InSb']['Sb-5p']+(1-x)*U_params['GaSb']['Sb-5p']
    
    with open(U_out_file,'w') as ui:
        json.dump(U_in,ui)
        
        
def write_LIU(U_base_file='U_base.json',U_out_file='U_in.json'):
    with open(U_base_file,'r') as ui:
        U_params=json.load(ui)
    U_in={}
    for i in range(5):
        x=float(i/4)
        y=float(i/4)
        U_in[f'In{i}-5p']=(1-y)*U_params['InSb']['In-5p']+(y)*U_params['InAs']['In-5p']
        U_in[f'Ga{i}-4p']=(1-y)*U_params['GaSb']['Ga-4p']+(y)*U_params['GaAs']['Ga-4p']
        U_in[f'As{i}-4p']=(1-x)*U_params['InAs']['As-4p']+(x)*U_params['GaAs']['As-4p']
        U_in[f'Sb{i}-5p']=(1-x)*U_params['InSb']['Sb-5p']+(x)*U_params['GaSb']['Sb-5p']
    with open(U_out_file,'w') as ui:
        json.dump(U_in,ui)
        
def main():
    parser = argparse.ArgumentParser(description='params')
    parser.add_argument('-x', dest='x', type=float, default=0.5)
    parser.add_argument('-y', dest='y', type=float, default=0.5)
    parser.add_argument('-N', dest='N', type=int,nargs=3, default=(3,3,3))
    parser.add_argument('--base', dest='base', type=str, default='none')
    parser.add_argument('--Uout', dest='U_out', type=str, default='none')
    parser.add_argument('--Ubase', dest='U_base', type=str, default='none')
    
    args = parser.parse_args()
    x=args.x
    y=args.y
    N=args.N
    base=args.base
    U_out_file=args.U_out
    U_base_file=args.U_base
    x=round(x,2)
    y=round(y,2)
    x1=round(1-x,2)
    y1=round(1-y,2)

    if base=='none':
        base="In%sGa%sAs%sSb%s_%sx%sx%s"%(x,x1,y1,y,N[0],N[1],N[2])
    if U_out_file=='none':
        U_out_file="%s.U_in.json"%base
    if U_base_file=='none':
        U_base_file="U_base.json"
    else:
        U_base_file=U_base_file
    print(U_base_file,U_out_file)
    write_Uin(x, y, U_base_file, U_out_file)

if __name__ == "__main__":
    main()
