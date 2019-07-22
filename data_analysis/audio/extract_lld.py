__author__ = 'Hayato Katayama'

import subprocess
from glob import glob
import pandas as pd

order = 'bash /Users/hayato/Downloads/openSMILE-2.3.0/SMILExtract '
config = '-C /Users/hayato/Downloads/openSMILE-2.3.0/emobase2010_csv_lld.conf '
columns = [str(i+1) for i in range(228)]

def extract_lld(INPUT,OUTPUT):
    #OUTPUT = INPUT.replace('wav','LLD')
    cmd =  order + config + '-I ' + INPUT + ' -O ' + OUTPUT
    print(cmd)
    try:
        res = subprocess.run(cmd, shell=True)
    except Exception as e:
        print("Runtime Error.")

def concat_lld(INPUT_A,INPUT_B):
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
    wav_files = sorted(glob('/Volumes/Untitled/WOZData/wav/20190703*'))
    for wav_f in wav_files:
        INPUT = wav_f
        OUTPUT = INPUT.replace('.wav','.lld.csv').replace('/wav','/LLD')
        extract_lld(INPUT=INPUT,OUTPUT=OUTPUT)

    lld_files = sorted(glob('/Volumes/Untitled/WOZData/LLD/20190703*'))
    for i in range(0,len(lld_files),2):
        df = concat_lld(INPUT_A = lld_files[i],INPUT_B = lld_files[i+1])
        df.to_csv(lld_files[i].replace('.A','.LLD'),index=False)
        print('generated>>',lld_files[i])
