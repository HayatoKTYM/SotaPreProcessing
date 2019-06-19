# -*- coding: utf-8 -*-

import numpy as np
import wave
import sys

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# ファイルパスもしくは波形データ（数値）を受け取り、その波形のスペクトログラムを計算する
# スペクトログラムはself.img_arrayに格納される
#
#

class Generator:

    def __init__(self, fs, frame_size, frame_shift, chunk_size):
        self.fs = fs
        self.frame_size = frame_size
        self.frame_shift = frame_shift
        self.chunk_size = chunk_size
        self.win = np.hanning(frame_size)
        self.img_array = []
        self.grayscale = []
        self.start_frame = None
        self.end_frame = None

    def fromNumData(self, num_data):

        # for i in range(len(num_data)):	## 高域強調
        #     num_data[i] = num_data[i] - 0.97 * num_data[i-1]

        frame_start = 0
        frame_end = self.frame_size
        chunk = num_data[frame_start : frame_end]
        img_array = []

        while len(chunk) >= self.frame_size:
            chunk = chunk * self.win
            chunk = np.hstack ([chunk, np.zeros((self.chunk_size-self.frame_size))])
            #print(chunk.shape)
            if chunk.shape[0] != self.chunk_size:
                break
            else:
                # normalized, windowed frequencies in data chunk
                spec = np.fft.rfft(chunk) / self.chunk_size
                # get magnitude
                psd = abs(spec)
                # convert to dB scale
                psd = 20 * np.log10(psd)

                psd = np.asarray([psd])

                if img_array == []:
                    img_array = psd
                elif img_array.shape == (self.chunk_size,):
                    img_array = np.asarray([img_array])
                    img_array = np.r_[img_array, psd]
                else:
                    img_array = np.r_[img_array, psd]

                    #print(img_array.shape)

            frame_start = frame_start + self.frame_shift
            frame_end = frame_end + self.frame_shift
            chunk = num_data[frame_start: frame_end]

        self.img_array = img_array

        self.grayscale = (img_array - np.min(img_array)) / (np.max(img_array) - np.min(img_array)) * 255

    def start_time2frame(self, start_time):
        self.start_frame = int(10 * start_time / (self.frame_shift * 1000 / self.fs) + 1)	##はじめに10かけているのは、qaのinputで100が1秒という風に合わせているから

    def end_time2frame(self, end_time):
        self.end_frame = int(10 * end_time / (self.frame_shift * 1000 / self.fs) - (self.frame_size * 1000 / self.fs)/(self.frame_shift * 1000 / self.fs))

    def fromFilePath(self, path):
        wf = wave.open(path, "rb")
        data = wf.readframes(wf.getnframes())
        num_data = np.fromstring(data, dtype = np.int16)
        wf.close()

        self.fromNumData(num_data)

class Continuous_Generator:
    # 連続的に波形が入ってくることを想定
    # 無駄にfft計算しないようにする
    def __init__(self, fs, frame_size, frame_shift, chunk_size, input_size, output_size):
        self.fs = fs
        self.frame_size = frame_size
        self.frame_shift = frame_shift
        self.chunk_size = chunk_size
        self.win = np.hanning(frame_size)
        self.img_array = np.asarray([])
        self.grayscale = []
        self.start_frame = None
        self.end_frame = None

        self.input_size = input_size
        self.output_size = output_size
        self.stack = np.asarray([]) # 大きさ frame_size + input_sizeの配列

        if input_size % frame_shift != 0:
            sys.stderr.write("Change the values for input_size divisible by frame_shift\n")
            sys.exit(1)

    def __call__(self, num_data):

        if self.stack.shape[0] < self.frame_size:
            self.stack = np.hstack([self.stack, num_data])


            if self.stack.shape[0] == self.frame_size:
                psd = self.get_psd(self.stack)
                self.img_array = psd
            elif self.stack.shape[0] > self.frame_size:
                # frame_size, input_size, output_sizeの整合性が取れてない場合のやつ。いらないかも
                psd = self.get_psd(self.stack[:self.frame_size])
                self.img_array = psd
            else:
                print('wait')


        elif self.stack.shape[0] >= self.frame_size:
            self.stack = np.hstack([self.stack[self.frame_shift:], num_data])

            start_frame = 0
            end_frame = self.frame_size
            chunk = self.stack[start_frame : end_frame]
            for i in range(self.input_size / self.frame_shift):
                psd = self.get_psd(chunk)
                self.img_array = np.r_[self.img_array, psd]

                start_frame = start_frame + self.frame_shift
                end_frame = end_frame + self.frame_shift

            print(self.img_array.shape)
            if self.img_array.shape[0] < self.output_size:
                return None

            elif self.img_array.shape[0] == self.output_size:
                return self.img_array

            elif self.img_array.shape[0] > self.output_size:
                self.img_array = self.img_array[(-1 * self.output_size) : ]

                return self.img_array



    def get_psd(self, chunk):
        chunk = chunk * self.win
        chunk = np.hstack ([chunk, np.zeros((self.chunk_size-self.frame_size))])

        # normalized, windowed frequencies in data chunk
        spec = np.fft.rfft(chunk) / self.chunk_size
        # get magnitude
        psd = abs(spec)
        # convert to dB scale
        psd = 20 * np.log10(psd)
        psd = np.asarray([psd])

        return psd
