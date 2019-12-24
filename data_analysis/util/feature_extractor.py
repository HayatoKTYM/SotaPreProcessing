# -*- coding: utf-8 -*-
"""
全ての特徴量をconcatしたファイルを生成する
label/
decode/
vad/
gaze/
"""

import glob
import pandas as pd
from argparse import ArgumentParser

def concat_feature(lf, df, vf, gf):
    df_label = pd.read_csv(lf)
    df_decode = pd.read_csv(df)
    df_vad = pd.read_csv(vf)
    df_gaze = pd.read_csv(gf)

    assert len(df_label) == len(df_decode), print('cannot concat files.')
    #print(0,len(df_label))
    df = pd.concat([df_label, df_decode, df_vad, df_gaze],axis=1)
    df = df.fillna(0)
    return df

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--datadir", type=str, metavar="DIRECTORY", required=False, default='/Volumes/Untitled/WOZData',
                        help="data directory")
    parser.add_argument("-o", "--outdir", type=str, metavar="DIRECTORY", required=False,
                        help="output directory", default="/Volumes/Untitled/WOZData/feature")
    parser.add_argument("--debug", required=False,
                        help="is debug", action='store_true')
    args = parser.parse_args()

    label_files = sorted(glob.glob(args.datadir + '/label/20190*.csv'))
    decode_files = sorted(glob.glob(args.datadir + '/decode/20190*.csv'))
    vad_files = sorted(glob.glob(args.datadir + '/vad/20190*.csv'))
    gaze_files = sorted(glob.glob(args.datadir + '/gaze/20190*.csv'))


    for lf, df, vf, gf in zip(label_files, decode_files, vad_files, gaze_files):
        print(lf.split('.')[-3].split('/')[-1])
        if lf.split('.')[-3].split('/')[-1] == vf.split('.')[-3].split('/')[-1] == \
                df.split('.')[-3].split('/')[-1] == gf.split('.')[-3].split('/')[-1]:

            datetime = lf.split('.')[-3].split('/')[-1]
            OUTPUT = "{}/{}.feature.csv".format(args.outdir, datetime)

            concat_df = concat_feature(lf,df,vf,gf)
            concat_df.to_csv(OUTPUT,index=False)
        else:
            print('error')
