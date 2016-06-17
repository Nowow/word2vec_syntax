# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 03:23:45 2016

@author: robert
"""


import pickle
import os
import re

# minicorpus - '/run/media/robert/1TB-1/linuxfolder/cash/rcorpora/post1950/archive/gaz/'

corporaDump = open('/run/media/robert/1TB-1/linuxfolder/pythonworks/miniCorp', 'ab')

for root, dirs, files in os.walk('/run/media/robert/1TB-1/linuxfolder/cash/rcorpora/post1950/archive/gaz/'):
    for fname in filter(lambda fname: fname.endswith('.conll'), files):
                

        document = open(os.path.join(root, fname), 'r')
        
        wordCounter = -1
        sentCash = []
        print(fname)
        
        for line in document:
            
#            print(len(line))
            if len(line)<5:
                if len(sentCash) > 1:
                    pickle.dump(sentCash, corporaDump)
                    
#                   print(sentCash)
                wordCounter = -1
                sentCash = []
                
#                print(line)
 #               print('yiss')
                continue
                    
            line = line.split()
            wordCounter += 1
           
            
            if wordCounter < int(line[0]):
                if re.match('[A-Za-zА-Яа-я]+$', line[2].lower()) != None:
                    sentCash.append(line[2])
            else:
#                print(len(line))
                
                
                wordCounter = -1
                sentCash = []

corporaDump.close()
                