#!/usr/bin/python
#coding:utf-8
import argparse


def getArgs():
    parser = argparse.ArgumentParser(description="ファイルを複数のファイルへ分割する。入力ファイルは複数あってもよい")

    parser.add_argument(
        "-f", "--input",
        dest="input_files",
        nargs="+",
        help="分割したいファイル"
    )

    parser.add_argument(
        "-o", "--output",
        dest="output_dir",
        required=True,
        help="出力ディレクトリ"
    )

    parser.add_argument(
        "-s", "--split-num",
        dest="split_num",
        type=int,
        required=True,
        help="分割する数"
    )

    parser.add_argument(
        "-n", "--split-name",
        dest="name",
        type=str,
        default="split",
        help="分割後の名前, [name].[num].txtになる"
    )

    return parser.parse_args()

args = getArgs()

# count sent 
sent_count = 0
for f in args.input_files:
    for line in open(f):
        if line.strip() == "":
            sent_count += 1

line_per_file = sent_count/args.split_num

# split and write
sent_count = 0
file_prefix = 0
outf = open("%s/%s.%d.txt" % (args.output_dir, args.name, file_prefix), "w")
for inf in args.input_files:
    for line in open(inf):
        if line.strip() == "":
            sent_count += 1
        if line_per_file == sent_count and file_prefix != args.split_num-1:
            file_prefix += 1
            sent_count = 0
            outf.close()
            outf = open("%s/%s.%d.txt" % (args.output_dir, args.name, file_prefix),"w")
        outf.write(line)
outf.close()

