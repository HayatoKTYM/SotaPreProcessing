__author__ = 'Hayato Katayama'
__date__ = '20190630'
"""
音声認識結果を集計して単語辞書を作る(word2id)
単語idに対してそれに対応する重み行列を作成

1. 音声認識結果を集計
2. MeCabで分かち書き(保存)
3. word2id, embedding_metrix
"""
import MeCab
import numpy as np
from glob import glob
import pandas as pd
mThings = MeCab.Tagger('Ochasen')
mThings.parse('')
import json, pickle

def wakati(sentences):
    """
    分かち書きして返す関数
    param: 私は学生です
    return: [私,は,学生,です]
    """
    texts = []
    m = MeCab.Tagger("-Ochasen")
    for sentence in sentences:
        word_list = list()
        words_chasen = m.parse(sentence).split('\n')
        for word_chasen in words_chasen:
            if word_chasen == 'EOS': break
            word = word_chasen.split("\t")[0]
            word_list.append(word)
        word_list = ' '.join(word_list)
        texts.append(word_list)
    return texts

def make_Embedding(tokenizer, EMBEDDING_DIM=300):
    """
    重み行列作成
    """
    embedding_metrix = np.zeros((len(tokenizer.word_index)+1,EMBEDDING_DIM))
    for word, i in tokenizer.word_index.items():
        try:
            embedding_vector = model[word]
            embedding_metrix[i] = embedding_vector
        except KeyError:#学習済みモデルにない単語は，乱数で値を決定
            print(word)
            embedding_metrix[i] = np.random.normal(0, np.sqrt(0.25), EMBEDDING_DIM)
    return embedding_metrix

def save_word2id(tokenizer, INPUT=''):
    """
    単語→idの辞書を保存
    """
    f = open(INPUT,'w')#.json
    json.dump(tokenizer.word_index,f)
    f.close()

def save_EmbeddingMetrix(embedding_metrix, INPUT=''):
    """
    分散行列の保存@python3
    """
    f = open(INPUT,"wb")#
    pickle.dump(embedding_metrix,f,protocol=2)
    f.close()

if __name__ == '__main__':
    label_files = sorted(glob('/Volumes/Untitled/WOZData/decode/*csv'))
    print(label_files)
    sentences = list()
    for lf in label_files:
        df = pd.read_csv(lf)
        sentences.extend(list(set(df['A'].values)))
        sentences.extend(list(set(df['B'].values)))
    sentences = list(set(sentences))
    sentences.remove('0')
    texts = wakati(sentences)

    #学習済み分散表現モデルの読み込み
    import gensim
    model = gensim.models.KeyedVectors.load_word2vec_format('/Users/hayato/Desktop/model.vec', binary=False)
    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.sequence import pad_sequences
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts) #各単語をidに変換
    sequence = tokenizer.texts_to_sequences(texts)
    #pad_sequenceでは、指定した数に配列の大きさを揃えてくれる,#指定した数より配列が大きければ切り捨て、少なければ０で埋める
    sequence = pad_sequences(sequence, maxlen=29)
    #embedding行列作成
    embedding_metrix = make_Embedding(EMBEDDING_DIM = 300, tokenizer = tokenizer)
    print(embedding_metrix.shape)
    #保存フェーズ
    save_word2id(tokenizer, INPUT='word_index.json')
    save_EmbeddingMetrix(embedding_metrix, INPUT='embedding_metrix.pkl')
    print('Generated >>> EMBEDDING METRIX')
