#!/usr/bin/python2.7

# insert only new tenses into the new database

import sys
import codecs
import csv
import mysql.connector

# global vars
infile = "A2_French_tenses.csv"
outfile = "insert_tenses_sql.txt"
language_id = 2
user_id = 1

# test user pass
cnx = mysql.connector.connect(user='root', 
                              password='mysql',
                              host='127.0.0.1',
                              database='language_flashcards',
                              charset='utf8')

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def getTenseNameId(tense_name):
  cursor = cnx.cursor()
  query = ("SELECT id FROM tense_name WHERE name like \""+tense_name+"\";")
  cursor.execute(query)
  value = cursor.fetchone()
  if cursor.rowcount > 0:
    cursor.close()
    print "FOUND "+tense_name
    return value[0]
  else:
    cursor.close()
    print "NOT EXIST "+tense_name
    return 0

def insertTenseName(tense_name):
  cursor = cnx.cursor()
  query = ("INSERT INTO `tense_name`( `language_id`, `name`) VALUES ("+str(language_id)+",\""+tense_name+"\")" )
  print query
  cursor.execute(query)
  cnx.commit()
  print "INSERT "+tense_name
  value = cursor.lastrowid
  cursor.close()
  return value

def getVerbId( verb ):
  cursor = cnx.cursor()
  query = ("SELECT id FROM verb WHERE infinitive like \""+verb+"\";")
  print query
  cursor.execute(query)
  value = cursor.fetchone()
  if cursor.rowcount > 0:
    cursor.close()
    print "FOUND "+verb
    return value[0]
  else:
    cursor.close()
    print "NOT EXIST "+verb
    return 0

def insertVerb( verb ):
  cursor = cnx.cursor()
  query = ("INSERT INTO `verb`( `infinitive`) VALUES (\""+verb+"\")" )
  print query
  cursor.execute(query)
  cnx.commit()
  print "INSERT "+verb
  value = cursor.lastrowid
  cursor.close()
  return value

def getTenseId(verb_id, tensename_id):
  cursor = cnx.cursor()
  query = ("SELECT id FROM tense WHERE tensename_id = "+str(tensename_id)+" and verb_id = "+str(verb_id)+";")
  print query
  cursor.execute(query)
  value = cursor.fetchone()
  if cursor.rowcount > 0:
    cursor.close()
    print "FOUND tense"
    return value[0]
  else:
    cursor.close()
    print "NOT EXIST tense"
    return 0

def insertTense(value, verb_id, tensename_id):
  cursor = cnx.cursor()
  query = ("INSERT INTO `tense`( `value`, `tensename_id`, `verb_id`) VALUES (\""+value+"\", "+str(tensename_id)+", "+str(verb_id)+")" )
  print query
  cursor.execute(query)
  cnx.commit()
  print "INSERT tense"
  value = cursor.lastrowid
  cursor.close()
  return value

def insertTenseGuess(tense_id, user_id): 
  cursor = cnx.cursor()
  query = ("INSERT INTO `tense_guess`( `user_id`, `tense_id`, `a2b_ok`, `a2b_ko`, `b2a_ok`, `b2a_ko`) VALUES ("+
  str(user_id)+", "+str(tense_id)+", 0, 0, 0, 0)" )
  print query
  cursor.execute(query)
  cnx.commit()
  print "INSERT tense"
  value = cursor.lastrowid
  cursor.close()
  return value

with codecs.open(infile, encoding='utf-8') as csv_file, codecs.open(outfile,"w", encoding='utf-8') as outf:
  csv_reader = unicode_csv_reader(csv_file, delimiter=',')

  # map that holds tenses ids
  tenses_ids = {}

  # search all tense names and insert them if not found
  for line in csv_reader:
    # first line, with just the name of the tenses
    if line[0] == "Infinitif":
      tense_order = 0
      for tense in line[1:]:
        tense_id = getTenseNameId(tense)
        if tense_id == 0:
          tenses_ids[ tense_order ] = insertTenseName(tense)
        else:
          tenses_ids [ tense_order ] = tense_id
        tense_order += 1
    # not first line
    else:
      # make sure the verb exists
      verb_id = getVerbId(line[0])
      if verb_id == 0:
        verb_id = insertVerb(line[0])

      #for each tense
      tense_order = 0
      for tense in line [1:]:
        tensename_id = tenses_ids[tense_order]
        tense_id = getTenseId(verb_id, tensename_id)
        if tense_id == 0:
          tense_id = insertTense(tense, verb_id, tensename_id)
          insertTenseGuess(tense_id, user_id)
        tense_order += 1
     
outf.close() 

cnx.close()
