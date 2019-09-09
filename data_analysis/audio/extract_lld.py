#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'Hayato Katayama'

import subprocess
from glob import glob
import pandas as pd
import argparse

order = 'bash /Users/hayato/Downloads/openSMILE-2.3.0/SMILExtract '
config = '-C /Users/hayato/Downloads/openSMILE-2.3.0/emobase2010_csv_lld.conf '
columns = [str(i+1) for i in range(228)]

def extract_lld(INPUT:str,OUTPUT:str):
    """
    :param INPUT: 入力ファイルPATH (.wav)
    :param OUTPUT: 出力ファイルPATH (.csv)
    :return:
    """
    cmd =  order + config + '-I ' + INPUT + ' -O ' + OUTPUT
    print(cmd)
    try:
        res = subprocess.run(cmd, shell=True)
    except Exception as e:
        print("Runtime Error.")

def concat_lld(INPUT_A:str,INPUT_B:str):
    """
    :param INPUT_A: AのLLD抽出ファイル
    :param INPUT_B: BのLLD抽出ファイル
    :return:
    """
    df_A = pd.read_csv(INPUT_A)
    df_B = pd.read_csv(INPUT_B)
    assert len(df_A) == len(df_B), print('Not a property file, you specify A & B LLD files?')

    df = pd.concat([df_A,df_B],axis=1)
    df.columns = columns
    return df

if __name__ == '__main__':
    """
    1. A,Bの音声からLLD特徴量抽出
    2. A,Bの特徴量ファイルをconcat
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', '-d', type=str, default='/mnt/aoni02/katayama/dataset/DATA2019/*wav',
                        help='specify the wav folder PATH')
    parser.add_argument('--out', '-o', type=str, default='/mnt/aoni02/katayama/dataset/DATA2019/LLD/*csv',
                        help='specify the LLD output folder PATH')

    print('Extaction Folder : {}'.format(args.dir))
    print('Output Folder : {}'.format(args.out))
    directory = glob(args.dir)
    output = args.out

    wav_files = sorted(glob(directory))
    for wav_f in wav_files:
        INPUT = wav_f
        OUTPUT = INPUT.replace('.wav','.lld.csv').replace('/wav','/LLD')
        extract_lld(INPUT=INPUT,OUTPUT=OUTPUT)

    lld_files = sorted(glob(output))
    for i in range(0,len(lld_files),2):
        df = concat_lld(INPUT_A = lld_files[i],INPUT_B = lld_files[i+1])
        df.to_csv(lld_files[i].replace('.A','.LLD'),index=False)
        print('generated>>',lld_files[i])
