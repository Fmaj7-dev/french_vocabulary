#!/usr/bin/python

# insert vocabulary (words or verbs) from a txt into the new database.

import sys
import codecs

infile = "words.txt"

# first free id in vocabulary database
vocabulary_offset = 1075
user_id = 1
category_id = 1

with codecs.open(infile, encoding='utf-8') as inf:
    for line in inf:
        v = line.split('#')
        french_replaced = v[0].replace('\'', '\\\'')
        spanish_replaced = v[1].replace('\n', '') 

        print("INSERT INTO `vocabulary` VALUES ("+str(vocabulary_offset)+", '"+french_replaced+"', '"+spanish_replaced+"', 2, 1, 3);")
        print("INSERT INTO `guess` (`user_id`, `vocabulary_id`, `a2b_ok`,`a2b_ko`,`b2a_ok`,`b2a_ko`) VALUES ("+str(user_id)+", "+str(vocabulary_offset)+", 0, 0, 0, 0);")
        print("INSERT INTO `vocabulary_category` (`vocabulary_id`, `category_id`) VALUES ("+str(vocabulary_offset)+", "+str(category_id)+");")

        vocabulary_offset += 1




