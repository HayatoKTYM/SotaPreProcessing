__author__ = "Hayato Katayama"
__date__    = "20190304"
import glob
import cv2, os
import pandas as pd
import keras

model = keras.models.load_model('/mnt/aoni02/katayama/short_project/proken2018_B/target/gazemodel_128.h5')


def predict_gaze(INPUT_FILES):
    """
    @param 1対話分の画像
    return 各画像の予測ラベル(正解ラベル)
    """
    label = []
    for file in INPUT_FILES:
        img = cv2.imread(file, 0).reshape(1, 32, 96, 1)
        prob = model.predict(img / 255.0)
        prob = 1 if prob[0] > 0.5 else 0
        label.append(prob)
    return label


if __name__ == '__main__':
    folders = glob.glob('/Volumes/Untitled/WOZData/eye/2018*')
    print(folders)
    for dir in folders:
        files = sorted(glob.glob(dir + '/*png'))[:]
        label = predict_gaze(files)
        df = pd.DataFrame({'path': files, 'gaze': label})
        path = dir.replace('eye', 'gaze')
        #if not os.path.exists(path):
        #    os.mkdir(path)
        OUTPUT = path + '.gaze.csv'
        df.to_csv(OUTPUT, index=False)
        print('Generated>>',OUTPUT)
