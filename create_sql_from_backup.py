#!/usr/bin/python2.7

# inserts words into the new database from the old one

import sys
import codecs

infile = "backup.sql"
outfile = "insert_sql.txt"

with codecs.open(infile, encoding='utf-8') as inf, codecs.open(outfile,"w", encoding='utf-8') as outf:
    for line in inf:
        v = line.split(',')
        v1 = v[1].replace('\'', '').lstrip()
        v2 = v[2].replace('\'', '').lstrip()
        v2 = v2.replace('\r\n', '')
        outf.write("INSERT INTO `vocabulary` (`id`, `word_a`, `word_b`, `language_a`, `language_b`, `level`) VALUES ('"
        +v[0]+"', '"+v1+"', '"+v2+"', 2, 1, 2 );\n")
