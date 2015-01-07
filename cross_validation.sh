#!/bin/sh

# bash ./cross_validation.sh -s -i 10 -t
# -s : ファイルの分割を行う（一度だけで良い）
# -t: tuningを行う
# 分割数の指定とパラメータの指定は別ファイルで指定する


# 設定ファイルの読み込み
if ! [ -e cross_info.conf ]
then
    echo "conf file not found"
    exit
fi
for line in `cat cross_info.conf | grep -v ^#`
do
    first=`echo ${line} | cut -d ':' -f 1`
    second=`echo ${line} | cut -d ':' -f 2`
    case $first in
        "DivisionNumber" ) VALUE_I=$second ;;
        "f" ) VALUE_F=$second ;;
        "c" ) VALUE_C=$second ;;
    esac
done


# オプション引数の解析
FLG_S="FALSE"
FLG_T="FALSE"
while getopts st OPT
do
    case $OPT in
        "s" ) FLG_S="TRUE" ;;
        "t" ) FLG_T="TRUE" ;;
    esac
done

if [ $FLG_S = "TRUE" ]
then
    [ -e tests ] && rm -r tests
    [ -e trains ] && rm -r trains
    [ -e models ] && rm -r models
    [ -e results ] && rm -r results
    [ -e diffs ] && rm -r diffs
    [ -e evaluations ] && rm -r evaluations
    [ -e onlyBI ] && rm -r onlyBI
    [ -e splits ] && rm -r splits
    [ -e dumps ] && rm -r dumps
    mkdir tests
    mkdir trains
    mkdir models
    mkdir results
    mkdir diffs
    #mkdir evaluations
    mkdir onlyBI
    mkdir splits
    #mkdir dumps
fi
if [ $FLG_T = "TRUE" ]
then
    [ -e tune ] && rm -r tune
    mkdir tune
    mkdir tune/models
    mkdir tune/results
    mkdir tune/conllevals
fi
[ -e conllevals ] && rm -r conllevals
mkdir conllevals


# 分割ファイルの作成
if [ $FLG_S = "TRUE" ]
then

    cd onlyBI
    echo create BI
    python ../scripts/get_BI_sent.py -1 ../labeled_data/* > temp
    python ../scripts/sort_BI_sent.py temp > result.txt
    rm temp
    python ../scripts/split_only_BI.py result.txt mix_file others $VALUE_I ../splits/ > ../splits/splits_info.txt
    cd ..

    # train, testファイル作成
    temp_i=`expr $VALUE_I - 1`
    for i in `seq 0 $temp_i`
    do
        echo "-----create test $i------"
        cat ./splits/split.$i.txt ./splits/split_other.$i.txt > ./tests/test.$i.txt
        echo "-----create train $i------"
        mv ./splits/split.$i.txt ./splits/temp
        cat ./splits/split.*.txt > ./trains/train.$i.txt
        mv ./splits/temp ./splits/split.$i.txt
    done
    echo "----merge mix file----"
    # ラベルをOに置き換えるのでは時間めっちゃかかるから、一度ラベルを消して付け直す方がいい
    #python ./scripts/merge_mix_to_train.py ./splits ./trains ./splits/splits_info.txt $VALUE_I
    #TODO
    # ラベルを削除
    # ラベル付けるための辞書の作り直し
    # ラベルを振り直す
    
    
    # train, testファイルの文数
    echo "-----train.txt sent count-----"
    for i in `seq 0 $temp_i`
    do
        echo "train.$i.txt"
        python ./scripts/sent_count.py ./trains/train.$i.txt
    done
    
    echo "-----test.txt sent count-----"
    for i in `seq 0 $temp_i`
    do
        echo "test.$i.txt"
        python ./scripts/sent_count.py ./tests/test.$i.txt
    done
fi


# チューニング
if [ $FLG_T = "TRUE" ]
then
    
    echo "-----------tune-----------"
    for c in 3 5 10 50 100 1000 10000
    do
        for f in 3 5 10 50 100 1000
        do
            echo "----tune: c=$c, f=$f----"
            crf_learn -t -p4 -f $f -c $c template trains/train.0.txt tune/models/model.$f.$c
    	    crf_test -m tune/models/model.$f.$c tests/test.0.txt > tune/results/result.$f.$c.txt
            perl ./scripts/conlleval.pl -d "\t" < tune/results/result.$f.$c.txt > tune/conllevals/eval.$f.$c
        done
    done
    
    python ./scripts/tune_best_f.py cross_info.conf temp.conf tune/conllevals/* > tune_result.txt
    mv temp.conf cross_info.conf
    for line in `cat tune_result.txt`
    do
        first=`echo ${line} | cut -d ':' -f 1`
        second=`echo ${line} | cut -d ':' -f 2`
        case $first in
            "f" ) VALUE_F=$second ;;
            "c" ) VALUE_C=$second ;;
        esac
    done
   
    echo "f:$VALUE_F, c:$VALUE_C" 
fi


echo "-----cross validation-----"
# ここからテスト
for i in `seq 0 $temp_i`
do
    #CRF++
    t1=`date +%s`
    echo "-----------train $i-----------"
    #crf_learn -t -a MIRA -p4 -f 3 -c 4.0 template train.$i.temp models/model.$i
    crf_learn -t -p4 -f $VALUE_F -c $VALUE_C template trains/train.$i.txt models/model.$i
    t2=`date +%s`
    echo `expr $t2 - $t1`sec
    t1=`date +%s`
    echo "-----------test $i-----------"
	crf_test -m models/model.$i tests/test.$i.txt > results/result.$i.txt
    t2=`date +%s`
    echo `expr $t2 - $t1`sec
    t1=`date +%s`
    echo "-----------diff $i-----------"
    mkdir diffs/$i
	python ./scripts/extract_fptn/diff.py results/result.$i.txt > diffs/$i/diff.txt
    python ./scripts/extract_fptn/spl_diff.py diffs/$i/diff.txt diffs/$i/
    python ./scripts/extract_fptn/get_tp.py results/result.$i.txt > diffs/$i/tp.txt
    python ./scripts/extract_fptn/get_word_from_diff.py diffs/$i/fp.txt > diffs/$i/temp_fp
    python ./scripts/extract_fptn/get_word_from_diff.py diffs/$i/tp.txt > diffs/$i/temp_tp
    python ./scripts/extract_fptn/get_word_from_diff.py diffs/$i/fn.txt > diffs/$i/temp_fn
    echo "tp" > diffs/$i/temp_tp2
    echo "\nfp" > diffs/$i/temp_fp2
    echo "\nfn" > diffs/$i/temp_fn2
    cat diffs/$i/temp_tp2 diffs/$i/temp_tp diffs/$i/temp_fp2 diffs/$i/temp_fp diffs/$i/temp_fn2 diffs/$i/temp_fn > diffs/$i/tpfpfn.txt
    rm diffs/$i/temp_tp2 diffs/$i/temp_tp diffs/$i/temp_fp2 diffs/$i/temp_fp diffs/$i/temp_fn2 diffs/$i/temp_fn

    t2=`date +%s`
    echo `expr $t2 - $t1`sec
    t1=`date +%s`
    echo "-----------grade $i-----------"
    #python ./scripts/eval.py results/result.$i.temp ./dumps/class_list.pkl ./dumps/eval.$i.dump diffs/$i> evaluations/eval.$i.txt
    perl ./scripts/conlleval.pl -d "\t" < results/result.$i.txt > conllevals/eval.$i
   
    t2=`date +%s`
    echo `expr $t2 - $t1`sec
done

t1=`date +%s`
echo "-------cross grade---------"
#python scripts/cross_grade.py ./dumps/eval.* > evaluations/cross_evaluation.txt
python scripts/conll_calc.py ./conllevals/* > conllevals/cross_evaluation.txt

t2=`date +%s`
echo `expr $t2 - $t1`sec



