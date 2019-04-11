#!/usr/bin/python2.7

# inserts words into the old database

import sys
import codecs

infile = "A2_French_words.txt"
outfile = "insert_sql.txt"

with codecs.open(infile, encoding='utf-8') as inf, codecs.open(outfile,"w", encoding='utf-8') as outf:
    for line in inf:
        v = line.split('#')
        v0 = v[0].replace('\'', '\\\'')
        v1 = v[1].replace('\n', '')
        outf.write("INSERT INTO `vocabulary` (`french`, `spanish`, `f2s_ok`, `f2s_ko`, `s2f_ok`, `s2f_ko`) VALUES ('"+v0+"', '"+v1+"', 0, 0, 0, 0);\n")
