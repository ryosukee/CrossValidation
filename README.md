これはCRF＋＋を使って交差検定を行うためのスクリプト郡です。  


### 使い方
1. このリポジトリをcloneするかDownloadするかして
2. labeled\_dataディレクトリにCRF++に入力する形式のラベル付きデータを入れる（複数ファイル可）  
(このとき、最初からある`replase_this_to_labeled_data`というファイルを消してください) 
3. template を自分が使うテンプレートに置き（書き）換える
4. ./cross\_validation.sh を実行  
例)  
`./cross_validation.sh -o > result`  

-o オプションをつけるとOのラベルしかついていない文を除きます。


### 結果
実行すると以下のディレクトリができます。  
* conlleval  
[conll2000のスクリプト][conll]を使って評価した結果が出力されます。  

* diffs  
間違えていた部分を抽出して出力しています。  
実際にデータを見て確かめたいときに見てください。   

* dumps  
計算するために必要な途中経過をdumpしたbinaryデータです。  
処理が終わったら基本的にもう必要ありません。  
eval.のファイルがdict, class\_list.pklがlistで、それぞれpythonのpickleモジュールでシリアライズしています。  

* evaluations  
自前で用意したgrade.pyスクリプトによって評価した結果が出力されます。  
cross\_evaluation.txtは交差検定のMacro平均とMicro平均の計算結果です。

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
`-o`オプションを指定した場合は、この時点でOのみの文は除外されています。  

* tests  
testデータとして使われたデータが出力されます。  

* trains  
trainデータとして使われたデータが出力されます。  


[conll]: http://www.cnts.ua.ac.be/conll2000/chunking/output.html


##### TODO
* 系列ラベリングなのにBとIを別々に評価してるのを直す  




