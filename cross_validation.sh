#!/bin/sh

# bash ./cross_validation.sh -o
# -o : training時にOのみのファイルを除外して, 同じsurfaceをtestとtrainの両方で出現しないようにする。

# オプション引数の解析
FLG_O="f"
VALUE_I=5
while getopts oi: OPT
do
    case $OPT in
        "o" ) FLG_O="TRUE" ;;
        "i" ) VALUE_I=$OPTARG ;;
    esac
done

[ -e tests ] && rm -r tests
[ -e trains ] && rm -r trains
[ -e models ] && rm -r models
[ -e results ] && rm -r results
[ -e diffs ] && rm -r diffs
[ -e evaluations ] && rm -r evaluations
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
#mkdir dumps

# Oのみの文を除外する
#if [ $FLG_O = "TRUE" ]
#then
    cd onlyBI
    echo create BI
    python ../scripts/get_BI_sent.py -1 ../labeled_data/* > temp
    python ../scripts/sort_BI_sent.py temp > result.txt
    rm temp
    python ../scripts/split_only_BI.py result.txt mix_file others $VALUE_I ../splits/ > ../splits/splits_info.txt
    cd ..
#else
# 除外せずに分割する
#    python ./scripts/split.py -f ./labeled_data/* -o ./splits -s 10
#fi

# 評価の時に必要なラベルのリストを作る
#python ./scripts/get_classes.py ./labeled_data/*


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
python ./scripts/merge_mix_to_train.py ./splits ./trains ./splits/splits_info.txt $VALUE_I

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


# ここからテスト
for i in `seq 0 $temp_i`
    do
#        echo "-----------$i-----------"
#        mv ./splits/split.$i.txt ./splits/test.$i.txt
#        cp ./splits/test.$i.txt ./tests
#        cat ./splits/split* > ./trains/train.$i.temp
#        if [ $FLG_O = "TRUE" ]
#        then 
#            # Oオプションがあったときに, trainファイルからOのみの文を除外する
#            python ./scripts/rm_only_O.py ./trains/train.$i.temp > ./trains/train.$i.temp2
#            rm ./trains/train.$i.temp
#            mv ./trains/train.$i.temp2 ./trains/train.$i.temp 
#        fi

        #CRF++
        t1=`date +%s`
        echo "-----------train $i-----------"
        #crf_learn -t -a MIRA -p4 -f 3 -c 4.0 template train.$i.temp models/model.$i
        crf_learn -t -p4 -f 3 -c 4.0 template trains/train.$i.txt models/model.$i
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



