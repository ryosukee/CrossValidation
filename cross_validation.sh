#!/bin/sh

# bash ./cross_validation.sh -o
# -o : training時にOのみのファイルを除外して, 同じsurfaceをtestとtrainの両方で出現しないようにする。

# オプション引数の解析
FLG_O="f"
while getopts o OPT
do
    case $OPT in
        "o" ) FLG_O="TRUE" ;;
    esac
done

[ -e tests ] && rm -r tests
[ -e trains ] && rm -r trains
[ -e models ] && rm -r models
[ -e results ] && rm -r results
[ -e diffs ] && rm -r diffs
#[ -e evaluations ] && rm -r evaluations
[ -e onlyBI ] && rm -r onlyBI
[ -e splits ] && rm -r splits
[ -e conllevals ] && rm -r conllevals
[ -e dumps ] && rm -r dumps

mkdir tests
mkdir trains
mkdir models
mkdir results
mkdir diffs
#mkdir evaluations
mkdir onlyBI
mkdir splits
mkdir conllevals
mkdir dumps

# Oのみの文を除外する
if [ $FLG_O = "TRUE" ]
then
    cd onlyBI
    echo create BI nolimit file
    python ../scripts/get_BI_sent.py -1 ../labeled_data/* > temp
    python ../scripts/sort_BI_sent.py temp > result.txt
    rm temp
    python ../scripts/split_only_BI.py
    cd ..
else
# 除外せずに分割する
    python ./scripts/split.py -f ./labeled_data/* -o ./splits -s 10
fi

# 評価の時に必要なラベルのリストを作る
#python ./scripts/get_classes.py ./labeled_data/*


# ここからテスト
for i in 0 1 2 3 4 5 6 7 8 9
    do
        echo "-----------$i-----------"
        mv ./splits/split.$i.txt ./splits/test.$i.txt
        cp ./splits/test.$i.txt ./tests
        cat ./splits/split* > ./trains/train.$i.temp
        if [ $FLG_O = "TRUE" ]
        then 
        # Oオプションがあったときに, trainファイルからOのみの文を除外する
        python ./scripts/rm_only_O.py ./trains/train.$i.temp > ./trains/train.$i.temp2
        rm ./trains/train.$i.temp
        mv ./trains/train.$i.temp2 ./trains/train.$i.temp 
        fi

        #CRF
        t1=`date +%s`
        echo "-----------train $i-----------"
        #crf_learn -t -a MIRA -p4 -f 3 -c 4.0 template train.$i.temp models/model.$i
        crf_learn -t -p4 -f 3 -c 4.0 template trains/train.$i.temp models/model.$i
        t2=`date +%s`
        echo `expr $t2 - $t1`sec
        t1=`date +%s`
        echo "-----------test $i-----------"
		crf_test -m models/model.$i splits/test.$i.txt > results/result.$i.temp
        t2=`date +%s`
        echo `expr $t2 - $t1`sec
        t1=`date +%s`
        echo "-----------diff $i-----------"
        mkdir diffs/$i
		python ./scripts/extract_fptn/diff.py results/result.$i.temp > diffs/$i/diff.txt
        python ./scripts/extract_fptn/spl_diff.py diffs/$i/diff.txt diffs/$i/
        python ./scripts/extract_fptn/get_tp.py results/result.$i.temp > diffs/$i/tp.txt
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
        perl ./scripts/conlleval.pl -d "\t" < results/result.$i.temp > conllevals/eval.$i
       
        t2=`date +%s`
        echo `expr $t2 - $t1`sec

        mv splits/test.$i.txt splits/split.$i.txt   
    done
t1=`date +%s`
echo "-------cross grade---------"
#python scripts/cross_grade.py ./dumps/eval.* > evaluations/cross_evaluation.txt
python scripts/conll_calc.py ./conllevals/* > conllevals/cross_evaluation.txt

t2=`date +%s`
echo `expr $t2 - $t1`sec



