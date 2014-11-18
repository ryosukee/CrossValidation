#!/bin/sh

# bash ./tune.sh -o
# -o : Oのみのファイルを除外しつつ同じsurfaceの文をtestとtrainで分けないようにする

# オプション引数の解析
while getopts o OPT
do
    case $OPT in
        "o" ) FLG_O="TRUE" ;;
    esac
done


mkdir tune
cd ./tune

[ -e tests ] && rm -r tests
[ -e trains ] && rm -r trains
[ -e models ] && rm -r models
[ -e results ] && rm -r results
[ -e diffs ] && rm -r diffs
[ -e evaluations ] && rm -r evaluations
[ -e onlyBI ] && rm -r onlyBI
[ -e splits ] && rm -r splits
[ -e conllevals ] && rm -r conllevals

mkdir tests
mkdir trains
mkdir models
mkdir results
mkdir diffs
mkdir evaluations
mkdir onlyBI
mkdir splits
mkdir conllevals

# Oのみの文を除外する
if $FLG_O then
    cd onlyBI
    echo create BI nolimit file
    python ../scripts/get_BI_sent.py -1 ../labeled_data/* > temp
    python ../scripts/sort_BI_sent.py temp > result
    rm temp
    python ../scripts/split_only_BI.py
    cd ..


else
# 除外せずに分割する
    python ./scripts/split.py -f ./labeled_data/* -o ./splits -s 10
fi

# 評価の時に必要なラベルのリストを作る
python ./scripts/get_classes.py ./labeled_data/*


# ここからテスト
for i in 0 1 2 3 4 5 6 7 8 9
    do
        echo $i
        mv ./splits/split.$i.txt ./splits/test.$i.txt
        cat ./splits/split* > ./trains/train.$i.temp

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
		python ./scripts/diff.py results/result.$i.temp > diffs/$i/diff.temp
        t2=`date +%s`
        echo `expr $t2 - $t1`sec
        t1=`date +%s`
        echo "-----------grade $i-----------"
        python ./scripts/grade.py results/result.$i.temp class_list.pkl evaluations/eval.$i.dump diffs/$i> evaluations/eval.$i.txt
        perl ./scripts/conlleval.pl < results/result.$i.temp > conllevals/eval.$i
       
        t2=`date +%s`
        echo `expr $t2 - $t1`sec
        


        mv splits/test.$i.txt splits/split.$i.txt   
    done
t1=`date +%s`
echo "-------cross grade---------"
python /home/r-miyazaki/work/asakawa/ryosuke/CRF/scripts/cross_grade.py evaluations/*.dump > evaluations/cross_evaluation
t2=`date +%s`
echo `expr $t2 - $t1`sec




