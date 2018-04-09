# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 11:46:21 2017

@author: Shawon

Parsing original data set

"""
import os, re, csv

word = re.compile("T.*CallOut.*")
word2 = re.compile("T.*Target.*")
word3 = re.compile("R.*Anaphoric_Relationship.*\n")

folder = 'C:\\Users\\Shawon\\Desktop\\CMV-Study\\data\\Set-1\\aa'
for filename in os.listdir(folder):
       infilename = os.path.join(folder,filename)
       if not os.path.isfile(infilename): continue
       with open(infilename, 'r', encoding = 'utf8') as f:
           print(f)
           a = []
           b = []
           c = []
           d = []
           e = []
           i = 0
           j = 0
           content = f.readlines()
           for line in content:
               a += re.findall(word, line)
               b += re.findall(word2, line)
               c += re.findall(word3, line)
           '''print(a)
           print('-----------------------')
           print(b)
           print('------------------------')
           print(c)
           print('------------------------')'''
           
           for k in c:
               match = re.search(r"(T\d+).*?(T\d+)", k)
               st = match.group(1)
               d.append(st)
               nd= match.group(2)
               e.append(nd)
           print(d)
           print(e)
           
           target = []
           for j in range(len(e)):
               pattern = e[j]
               #print(pattern)
               for item in b:
                   if re.match(pattern+'\t', item):
                      target.append(item)
                   else: continue
           #print(target)
           
           callout = []
           for i in range(len(d)):
               pattern2 = d[i]
               #print(pattern2)
               for itemi in a:
                   if re.match(pattern2+'\t', itemi):
                       callout.append(itemi)
                   else: continue
           #print(callout)
                   
           rows = zip(target, callout, c)
           #print(rows)
           #print(f)
           ff = os.path.splitext(os.path.basename(infilename))[0]
           #print(ff)
           suffix = '.csv'
           ff2 = os.path.join(ff + suffix)
           #print(ff2)
           f2 = open(ff2, 'w', encoding='utf8', newline = '')
           writer = csv.writer(f2, lineterminator = '\n')
           for row in rows:
               writer.writerow(row)
               #print(row)
           print(f)
           print('______________________________')
           
f2.close()
f.close()
