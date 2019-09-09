# README #
**収集データの前処理プログラム**


##音声から音響特徴量抽出
tksnack or opensmile

##画像から目部分切り出し
ffmpeg +
opncv + openface

##動画，音声，wizardの操作ログ(教師ラベル)の時間同期(the most important)


抽出した特徴量はcsvファイルに書き出す

各フォルダの説明
    /audio
           LLD特徴量の抽出
           VADラベルの抽出
           spectrogramの抽出
           .pcm -> .wav ファイル

    /label
           ロボットの行動ラベル抽出
           ロボットの顔向きラベル抽出
           ロボットの発話履歴抽出
           ユーザの音声認識結果抽出

    /video
           .avi -> .mp4 ファイル
           動画を画像に切り出すプログラム
           画像から顔を切り出すプログラム
           顔画像から目画像を切り出すプログラム
           目画像からラベルを自動生成するプログラム
    /util
           各csv file を統合する(concat)プログラム
           時間同期(音声，画像，操作ログ)プログラム

