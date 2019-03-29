#!/usr/bin/python

import sys
import codecs
import mysql.connector

# test user pass
cnx = mysql.connector.connect(user='root', 
                              password='mysql',
                              host='127.0.0.1',
                              database='french',
                              charset='utf8')


cursor = cnx.cursor()
query = ("SELECT * FROM verbs;")
cursor.execute(query) 

outfile = "insert_sql.txt"
offset = 551

with codecs.open(outfile,"w", encoding='utf-8') as outf:
  for (id_, french, spanish, fok, fko, sok, sko) in cursor:
    spanish_replaced = spanish.replace('\n','').replace('\r','').replace('\'', '\\\'')
    french_replaced = french.replace(',', '\,').replace('\'', '\\\'')

    id_offset = id_ + offset

    print("INSERT INTO `vocabulary` VALUES ("+str(id_offset)+", '"+french_replaced+"', '"+spanish_replaced+"', 2, 1, 2);")
    print("INSERT INTO `guess` VALUES ("+str(id_offset)+", 1, "+str(id_offset)+", "+str(fok)+ ", "+str(fko)+ ", "+str(sok)+", "+str(sko)+");")
    print("INSERT INTO `vocabulary_category` VALUES ("+str(id_offset)+", "+str(id_offset)+", 2);")

cursor.close()

cnx.close()



