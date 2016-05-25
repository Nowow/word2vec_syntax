# -*- coding: utf-8 -*-
"""
Created on Tue May 24 22:43:11 2016

@author: robert
"""

import pickle
import os
import re
import collections
# use nltk.download() to download stopwords corpus if not yet

from nltk.corpus import stopwords


# Iterable to be passed to word2vec class as sentences.
# reads sentences one by one from picke dump

class SentIterable(object):
    
# correct path to parsed corpus dump HERE

    dumpPath = '/run/media/robert/1TB-1/linuxfolder/pythonworks/corpusDump'
#    pickleDump = open(dumpPath, 'rb')
    
# self.sentCount to be inherited (got?) while creating context 86468867
    def __iter__(self):
        for sent in range(self.sentCount):
            yield pickle.load(self.pickleDump)


stops = set(stopwords.words('russian'))

# Looping over the corpus and generating pickle dump file that would give off
# context pairs one by one

def createContext(root_directory):
    
    pickleDump = open('/run/media/robert/1TB-1/linuxfolder/pythonworks/pickleDump', 'ab')
    dumpCounter = 0

# walking the corpus dir
# files walked linewise


    for root, dirs, files in os.walk(root_directory):
            for fname in filter(lambda fname: fname.endswith('.conll'), files):
                

                document = open(os.path.join(root, fname), 'r')
                
                
                
                wordCounter = -1
                sentDict = {}
                sentCash = []
                for line in document:
 
                    if len(line)<5:
                        continue
                    
                    line = line.split()
                                        # Creating cash dictionary for sentence

                    wordCounter += 1
                    if wordCounter < int(line[0]):

                        if re.match('[A-Za-zА-Яа-я]+$', line[2]) != None:
                            sentDict.update({line[0]:{'word':line[2],'ref':line[6]}})

                            
                        else:
                            sentDict.update({line[0]:{'word':None,'ref':line[6]}})

                            
                    else:
                        wordCounter = 0
                                            # Creating a sentence (context pair) to be passed to word2vec later
                        for slot in sentDict:
                            if sentDict[slot]['word'] == None:
                                continue
                            if sentDict[slot]['word'] in stops:
                                
                                continue
                            sentCash.append(sentDict[slot]['word'])
                            if (sentDict[slot]['ref'] != 0 and sentDict[slot]['ref'] != '0'):

                                try:
                            
                                    sentCash.append(sentDict[sentDict[slot]['ref']]['word'])
                                except:
                                    continue
                            for slot2 in sentDict:
                                if sentDict[slot2]['ref'] == slot:
                                    if sentDict[slot2]['word'] != None:
                                        if re.match('[A-Za-zА-Яа-я]+$', sentDict[slot2]['word']) != None:
                                            if sentDict[slot2]['word'] not in stops:
                                                sentCash.append(sentDict[slot2]['word'])
                                                # stopword check not working here, dont know why
                                                # recheck
                            for k in filter(lambda k: k in stops, sentCash):
                                sentCash.remove(k)
                            if len(sentCash) > 1:
                                pickle.dump(sentCash,pickleDump)
                                dumpCounter += 1
                            sentCash = []
                        sentDict = {}
                        if re.match('[A-Za-zА-Яа-я]+$', line[2]) != None:
                            sentDict.update({line[0]:{'word':line[2],'ref':line[6]}})
                        else:
                            sentDict.update({line[0]:{'word':None,'ref':line[6]}})

    pickleDump.close()
    return(dumpCounter)
                            
                        
                    
                            
                        
                    
                    
                                    
            
            
            
            
      
