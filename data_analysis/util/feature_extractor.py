# -*- coding: utf-8 -*-
"""
全ての特徴量をconcatしたファイルを生成する
"""
from __future__ import print_function
import glob
import csv
from argparse import ArgumentParser

class FeatureExtractor(object):
    def __init__(self, *filenames):
        self.filenames = list(filenames)
        self.fi = []
        self.labels = []
        for f in self.filenames:
            self.fi.append(csv.reader(open(f, 'r')))
        for reader in self.fi:  # ラベルだけ先に抽出
            self.labels += reader.next()

    def __iter__(self):
        return self

    def next(self):
        feature = []
        for reader in self.fi:
            feature += reader.next()
        return feature


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("-d", "--datadir", type=str, metavar="DIRECTORY", required=False, default='../../dataset',
                        help="data directory")
    parser.add_argument("-o", "--outdir", type=str, metavar="DIRECTORY", required=False,
                        help="output directory", default="../../dataset/feature")
    parser.add_argument("--debug", required=False,
                        help="is debug", action='store_true')

    args = parser.parse_args()

    audio_dir = args.datadir + '/audio'
    kinect_dir = args.datadir + '/kinect'
    label_dir = args.datadir + '/label'#_decode'
    vad_dir = args.datadir + '/vad'
    cam_dir = args.datadir + '/cam'

    audio_files = glob.glob(audio_dir + '/*.csv')
    kinect_files = glob.glob(kinect_dir + '/*.csv')
    label_files = glob.glob(label_dir + '/*.csv')
    vad_files = glob.glob(vad_dir + '/*.csv')
    cam_files = glob.glob(cam_dir + '/*.csv')
    print(len(audio_files))
    #print(audio_files[0].split(".")[-3].split("/")[-1])
    #print(kinect_files[0].split(".")[-3].split("/")[-1])
    #print(label_files[0].split(".")[-3].split("/")[-1])
    #print(vad_files[0].split(".")[-3].split("/")[-1])
    actions = []

    for lf, vf, af, kf, cf in zip(label_files, vad_files, audio_files, kinect_files, cam_files):
        print(lf.split('.')[-3].split('/')[-1])
        if lf.split('.')[-3].split('/')[-1] == vf.split('.')[-3].split('/')[-1] == \
                af.split('.')[-3].split('/')[-1] == kf.split('.')[-3].split('/')[-1] \
                 == cf.split('.')[-3].split('/')[-1] :
            datetime = lf.split('.')[-3].split('/')[-1]
            with open("{}/{}.feature.csv".format(args.outdir, datetime), 'w') as fo:
                extractor = FeatureExtractor(lf, vf, af, kf, cf)
                print(",".join(extractor.labels), file=fo)
                for f in extractor:
                    actions.append(f[0])
                    print(",".join(f).replace("nan", "0").replace("inf", "0"), file=fo)

        else:
            print("Error")

    from collections import Counter
    ac_counter = Counter(actions)
    print(ac_counter)
