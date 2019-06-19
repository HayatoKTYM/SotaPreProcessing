# -*- coding: utf-8 -*-
from __future__ import print_function
"""
行動タイプラベル，ターゲットラベルを生成するスクリプト
"""
__author__ = "Hayato Katayama"
__date__    = "20190304"

import pandas as pd
from datetime import timedelta
import sys,time
sys.path.append("..")

from util.frame_generator import FrameGenerator
from util.time_keeper import *
from util.file_reader import FileReader

from glob import glob

utterance_labels = ["None", "Passive", "Active", "Nod"]
target_labels = ["A", "B"]

DialogAct = {
    "recommendation-active"  : "Active",
    "detail-active"           : "Active",
    "question"          : "Active",
    "yes"               : "Passive",
    "no"                : "Passive",
    "unknown"           : "Passive", #change(Other)
    "pardon"            : "Passive", #change(Other)
    "followup"          : "Active",
    "start"          : "Active",
    "summarize"      : "Active",
    "nod"            : "Nod",
    "continue"       : "Continue",
    #"SpReco"         : "None",
    #"SpeakEnd"        : "Continue",
    "change_genre" : "Passive",
    "change_topic" : "Passive",
    "response-passive":"Passive",
    "abstract-correction"          : "Passive",
    "recommendation-correction"    : "Passive",
    "title-correction"             : "Passive",
    "genre-correction"             : "Passive",
    "review-correction"            : "Passive",
    "evaluation-correction"        : "Passive",
    "director-correction"          : "Passive",
    "actor-correction"             : "Passive"
}


class EventLog(object):

    def __init__(self, filename):
        self.raw_data = pd.read_csv(filename, header=None, names=('time', 'action', 'topic', 'target', 'utterance'),
                                    dtype={'time' : str, 'action' : str, 'topic' : str, 'target' : str, 'utterance' : str})
        self.start_row = 0
        self.end_row = 0
        self.start_time = 0
        self.end_time = 0
        self.datetime = ""  # 会話開始の時刻を識別子として利用
        self.data = self.split(filename)

    def split(self, filename):
        '''
        会話の開始(start)から終了(end)までのログを切り出す
        :return: 該当部分のログ (pandas.DataFrame)
        '''
        for i, v in self.raw_data.iterrows():
            if v['action'] == 'start':
                self.start_row  = i
                self.datetime = v['time'].split(".")[0]
                self.start_time = set_time(v['time'])
            elif v['action'] == 'end':
                self.end_row  = i
                self.end_time = set_time(v['time'])
                break

        return (self.raw_data[self.start_row:self.end_row+1].loc[(self.raw_data.action!="change_topic")])\
                    .loc[(self.raw_data.action!="change_genre")].loc[self.raw_data.utterance!="Recognizing"]\
                    .loc[(self.raw_data.action!="SpReco")]
            # (self.raw_data.action!="SpeakEnd") & (self.raw_data.action!="change_topic")]

    def to_list(self, dataframe):
        return dataframe.as_matrix().tolist()

def main():
    #f = open("decode.txt","w")
    directory = sorted(glob('/Users/hayato/Desktop/0131/1*'))
    #print(directory)

    for num in directory:
        print(num)
        num = "/Users/hayato/Desktop/0131/1"
        #setting_file = glob(num+"/*a.txt")[0]
        act_file = glob(num+"/*[!A].csv")[0]

        eventlog = EventLog(act_file)
        tk = TimeKeeper(act_file)
        output_file = act_file.split("/")[-1].split('.')[0]

        fo = open("/Users/hayato/Desktop/0131/label/{}.label.csv".format(tk.recording_datetime), "w")
        print("action,target,U", file=fo)
        f_genenrator = FrameGenerator(tk.start_time, tk.end_time,frame_rate=100)

        target = "A"
        action = ""
        utterance = ""
        lkcount = 0
        flag = 0
        event_list = eventlog.data.as_matrix().tolist()

        for f_time in f_genenrator:#フレーム単位ごとに
            log_time = set_time(event_list[0][0])#logにあるイベント
            if f_time >= log_time:
                event = event_list.pop(0)
                action = event[1]
                target = event[3][0]
                utterance = event[4]
                if utterance == "NONE": utterance = 0


            else:
                if action in DialogAct and flag==1:
                    pass
                else:
                    action = "None"

            if action in DialogAct:
                act_label = DialogAct[action]
                if flag == 1:#passive,Active,Nod行動中
                    act_label += "-Continue"
                elif act_label == "Nod":#Nod
                    print('nod')
                    utter_label = 0
                    #flag = 1
                elif act_label in ["Active","Passive"]:#行動開始タイミング
                    #print(utterance)
                    utter_label = utterance
                    flag = 1
                    #print("utterance",utterance)

                else:
                    #ここには分岐しないはず(一応)
                    utter_label = 0

            elif action == "look":
                act_label = "None"
                #continue
            else:#行動しない
                act_label = "None"
                utter_label = 0
                flag = 0

            print("{},{},{}".format(act_label, target,utter_label), file=fo)


            if action == "SpeakEnd":
                flag = 0
        fo.close()

if __name__ == '__main__':
    # EL = EventLog("data/20170731_1.csv")
    main()