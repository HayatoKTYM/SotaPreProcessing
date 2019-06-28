# -*- coding: utf-8 -*-

"""
AVI形式の動画ファイルを指定された開始時刻と
動画の時間を基に切り出して吐き出す
(出力はMP4形式推奨)
"""
__author__ = "Hayato Katayama"
__date__    = "20190304"

import subprocess
import sys
import logging
import glob

sys.path.append('..')

from util.time_keeper import TimeKeeper




def split_video(INPUT="", OUTPUT="", START="0.0", DURATION="0.0"):
    if INPUT == "" or OUTPUT == "" or DURATION == "0.0":
        logging.exception("*** Cutting the video :: Argument setting incorrect ***")
    else:
        command = "ffmpeg -ss " + START + " -i " + INPUT + " -t " + DURATION + " " + OUTPUT
        print("Command >> {}".format(command))
        subprocess.run(command, shell=True)


if __name__ == '__main__':
    folders = glob.glob('/Volumes/IWSDS2019/WOZRawData/07*')
    print(folders)
    for dir in folders:
        files = glob.glob(dir + '/*')
        for file in files:
            act_file = glob.glob(file + "/*[!A].csv")[0]
            movie_file = glob.glob(file + "/*.avi")[0]

            TK = TimeKeeper(act_file)
            movie_start = TK.get_diff_movie(movie_file)

            output_file = "/Volumes/IWSDS2019/WOZData/mp4/" + TK.recording_datetime + ".mp4"
            split_video(INPUT=movie_file, OUTPUT=output_file, START=str(movie_start), DURATION=str(TK.duration_sec))

            print("Output >> {}".format(output_file))
