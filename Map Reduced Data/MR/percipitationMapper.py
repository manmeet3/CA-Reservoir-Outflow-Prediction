#!/usr/bin/python

# The mapper
import sys
import csv
import os
import glob

path = '.'
extension = 'csv'
os.chdir(path)
csvFiles = glob.glob('*.{}'.format(extension))
print(csvFiles)
dict = {}
for file in csvFiles:
#file = 'BGP.csv'
    print(file)

    sensor_name = file.split('.')[0]

    previousLine = ''
    fxMap = []
    indexList = []
    SNOW = ""

    #for file in csvFiles:
    infile = open(file, 'r', encoding='ISO-8859-1')
    #infile = sys.stdin
    #infile = infile.encode('utf-8')

    next(infile) # skip the first line of input file
    count = 0;
    #print(len(infile))
    for line in infile:

        line = line.strip()
        line = line.split(',')

        try:
            if line[8].rstrip() == 'INCHES':
                # Get the data from line
                # print(line[6])
                #SNOW = line[6].rstrip()
                SNOW = line[6].rstrip()
                currentKey = sensor_name+'-'+line[4].rstrip()[:8]
                #print(SNOW)
                #print(currentKey)
                #if currentKey == 'ALP-20100201':
                #    break
                #print('previousLine: ', previousLine)
                #print(currentKey)
                dict[currentKey] = SNOW

            else:
                continue

        except Exception as e:
            print(e)


c = 0
for i in dict:
    c+=1
    #print(i, dict[i])
    fxMap.append(tuple([i, dict[i]]))
print(c)

for i in sorted(fxMap):
    print(i[0] , " :- " , i[1])
