これはCRF＋＋を使って交差検定を行うためのスクリプト郡です。  


##### TODO
* conllevalの交差検定のMicro平均値を計算, 出力する  
* 入力データの区切り文字をdオプションによる指定（タブと空白）  
* コードのリファクタリング（非常に読みづらい）

### 使い方
1. このリポジトリをcloneするかDownloadするかして
2. labeled\_dataディレクトリにCRF++に入力する形式のラベル付きデータを入れる（複数ファイル可）  
(このとき、最初からある`replase_this_to_labeled_data`というファイルを消してください) 
3. template を自分が使うテンプレートに置き（書き）換える
4. cross\_info.confを設定する  
5. ./cross\_validation.sh を実行

### オプション
* t: チューニングを行う
* s: ファイルの分割を行う（最初は必須）

例)  
`./cross_validation.sh -t -s > result`  

### チューニング
分割した一部のファイルを使ってCRF++のパラメータ（c, f）のチューニングを行う  
結果はtune\_result.txtに出力され、自動でcross\_info.confのパラメータ設定も書き換えます。  

### 設定（cross\_info.conf）
cross\_info.confに交差検定の設定を記述します。  
用意されてるファイルの数字だけ書き換えて使ってください。  
* DivisionNumber:分割数
* f: CRF++のパラメータf
* c: CRF++のパラメータc
* split\_type: 分割の方法  
  0: 厳格に分割する。testに含まれる正例はtraining時には隠す
  1: 単純に分割する。


### 注意
* 入力データの区切り文字は半角スペースのみ対応しています, タブ区切りでは区切り
を認識しません。


### 結果
実行すると以下のディレクトリができます。  
評価結果はconllevalに出力されます。  

* conlleval  
[conll2000のスクリプト][conll]を使って評価した結果が出力されます。  
conll\_calc.pyを使って交差検定のMacro平均値をcross\_evaluation.txtに出力しています。  

* diffs  
tp, fp, fnの事例を出力しています。  
diff.txtは間違えた事例全てです。  
実際にデータを見て確かめたいときに見てください。   

* models  
学習したモデルが出力されます。  

* onlyBI  
`-o`オプションを指定した場合にOのラベルしか振られていない文を除外するために一時的に出力するディレクトリです。  
B, Iが振られている語がファイル名になっています。  
覗いてみるとどの語にどのラベルが振られているのか、がなんとなくわかると思います。 
result.txtにはどの語にどのラベルがどれだけ振られているかが書かれています。   

* results  
CRF＋＋でtestした結果が出力されます。  

* splits  
labeled\_dataに入れたデータを10分割したデータが出力されます。  

* tests  
testデータとして使われたデータが出力されます。  

* trains  
trainデータとして使われたデータが出力されます。  
`-o`オプションを指定した場合は、ここでOのみの文は除外されています。  

[conll]: http://www.cnts.ua.ac.be/conll2000/chunking/output.html

