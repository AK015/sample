Windows上で実行
# 0. ディレクトリ構造 (sample1以下)
    ./datasets/
        000_dataset
        010_test
    ./code/
        generic/
            - arghelper.py
            - myfunction.py
            - mylogger.py
        json/
        log/
        summary/
            - history.md
            - README.md
            - requirements.txt
        - latest_log.txt

- `./dataset/` : datasetや各プログラムの出力が保存されるディレクトリ．
- `./dataset/000_dataset/` : 元となるデータセットの入ったディレクトリ．
- `./dataset/010_test/`   : データセットの画像から正方形を切り抜いて画像上にファイル名をプロットした画像が保存されるディレクトリ．`010_test.py`の実行結果が実行した日付別に保存される．
- `./code/generic/` : 関数などが定義されたファイルを保存するためのディレクトリ．
- `./code/generic/arghelper.py` : argparseを補助する関数などが定義されたファイル．円滑に研究を進めるための関数．
- `./code/generic/myfunction.py` : 各プログラムで使う関数などが定義されたファイル．
- `./code/generic/mylogger.py` : オリジナルのloggerクラスやログ用のデコレクタを定義したファイル．円滑に研究を進めるために役立つ．
- `./code/json/` : 各プログラムのコマンドライン引数用jsonファイルが格納されたディレクトリ．各プログラムにおいて`--args_save`をつけて実行することでjsonファイルごと自動生成される．
- `./code/log/`     :   各プログラムのログファイルの保存先．プログラムを実行することでログファイルと同時に自動生成されるディレクトリ．
- `./code/summary/`    :   記録用テキストファイルなどの保存先．
- `./code/summary/history.md`   :   プログラムなどの変更履歴を手動で記録するためのファイル．
- `./code/summary/README.md`    :   プログラムの使い方などを記録するためのファイル．
- `./code/summary/requirements.txt`  :   必要なパッケージなどが記録用されたファイル．`pip install -r requirements.txt`で一括インストール可能．
- `./code/latest_log.txt`    :   linuxで実行した場合，ログファイルと共に自動生成される．最新のログファイルへのショートカット(シンボリックリンク)．

※ 基本プログラムは(*lin*)シェルスクリプト経由(例)`./01_dataset_format.sh`，または(*win*)bat/vbsファイル経由で実行

# 1. 環境の準備
## 1.1. main環境
sample用のconda環境下で，以下のコマンドを順番に実行．

    pip install -r requirements.txt

データセットは，`./datasets/000_dataset/dataset_01/0XX.jpg`のようなディレクトリ構造で保存．
**City Walk Dataset**は[ここ](https://github.com/olly-styles/Multiple-Object-Forecasting)からダウンロードしていたが，2024/05/07現在はダウンロードできなくなっている．

# 2. データセットの画像から正方形を切り抜いて画像上にファイル名をプロット
(*lin*)以下のコマンドを実行．あるいは，(*win*)`010_test.bat`か`010_test.vbs`をダブルクリックすることで実行．

    ./010_test.sh

## 2.1. 関連ファイル
- `010_test.py` : main関数が定義されている．
- `./code/json/010_test.json` : コマンドライン引数がまとめられている．`--args_save`で自動生成・更新可能．
- `./code/generic/myfunction.py` : main関数で呼び出す関数が定義されている．コマンドライン引数もこのファイル内(get_args_for_xx関数)で設定している．

## 2.2. 実行時に調整する必要のあるコマンドライン引数
`./code/json/010_test.json`内の該当箇所を修正．
- `--input_dir` : 入力するデータセットのディレクトリを選択．

## 2.3. 出力
- `./datasets/010_test/` : このディレクトリ以下に日付ごとのディレクトリが生成され，その下に元のデータセットと同じ構造で処理後の画像が出力される．
- `./code/log/010_test/` : このディレクトリ以下にログファイルが生成される．なお，ディレクトリ自体も自動生成される．`010_test.py`のline:12で`log_save=False`とすることで生成されなくなる．
- `./code/lataset_log.txt` : (*lin*のみ)最新のログファイルへのショートカット(シンボリックリンク)が生成される．
- `./coed/json/010_test.json` : `--args_save`を渡した時のみ自動生成・更新される．

