__author__ = "Hayato Katayama"
__date__    = "20190304"

import cv2, os
import pandas as pd
import keras

model = keras.models.load_model('/Users/hayato/shortproject/GazeDetection/keras/gaze_1017_middle50.h5')


def predict_gaze(files):
    """
    @param 1対話分の画像
    return 各画像の予測ラベル(正解ラベル)
    """
    label = []
    for file in files:
        img = cv2.imread(file, 0).reshape(1, 32, 96, 1)
        prob = model.predict(img / 255.0)

        label.append(np.argmax(prob[0]))
    return label


if __name__ == '__main__':
    folders = glob.glob('/Users/hayato/Desktop/eye/*')
    print(folders)
    for dir in folders:
        files = sorted(glob.glob(dir + '/*png'))[:]
        label = predict_gaze(files)
        df = pd.DataFrame({'path': files, 'gaze': label})
        path = dir.replace('eye', 'gaze')
        if not os.path.exists(path):
            os.mkdir(path)
        df.to_csv(path + '/a.csv', index=False)
