# -*- coding: utf-8 -*-
"""
音声ファイルの切り出し
pcm -> wav
"""

import subprocess
import sys
import argparse
from glob import glob

sys.path.append('../')
from util.time_keeper import TimeKeeper

########################
# config
SAMPLING_RATE = 16000
CH = 1
BITS = 16
ch2spkr = {"ch1": "A", "ch2": "B"}


def split_pcm(input_file, output_file, start, duration):
    cmd = "sox -r {} -c {} -b {} -e signed-integer -t raw {} {} trim {} {}".format(
        SAMPLING_RATE, CH, BITS, input_file, output_file, start, duration)
    print(cmd)
    try:
        res = subprocess.run(cmd, shell=True)
    except Exception as e:
        print("Runtime Error.")
        print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', '-d', type=str, default='/mnt/aoni02/katayama/dataset/RawDATA/*',
                        help='specify the conversation folder PATH')
    parser.add_argument('--out', '-o', type=str, default='/mnt/aoni02/katayama/dataset/DATA2019/wav/',
                        help='specify the output folder PATH')

    print('Extaction Folder : {}'.format(args.dir))
    print('Output Folder : {}'.format(args.out))
    directory = glob(args.dir)
    output = args.out
    for i in directory:
        number = glob(i + "/*")
        for num in number:
            act_file = glob(num + "/*[!A].csv")[0]
            pcm_file = glob(num + "/000*")
            vad_file = pcm_file[0] + '/vad.txt'
            pcm_a = pcm_file[0] + "/ch1.pcm"
            pcm_b = pcm_file[0] + "/ch2.pcm"
            #時間同期を取るclass(TimeKeeper)
            TK = TimeKeeper(act_file)
            wav_start = TK.get_diff_sound(vad_file)

            #出力PATHの指定 & 変換の実行
            out_file = output + TK.recording_datetime + ".A" + ".wav"
            split_pcm(pcm_a, out_file, wav_start, TK.duration_sec)
            out_file = output + TK.recording_datetime + ".B" + ".wav"
            split_pcm(pcm_b, out_file, wav_start, TK.duration_sec)

            print("Genetared >> ", out_file)
