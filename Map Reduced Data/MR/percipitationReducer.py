#!/usr/bin/env python

from operator import itemgetter
import sys
import re
import csv



# Month Average
file= ''
prevMonth = ''
count = 0.00
prevCount = 0.00

infile = sys.stdin

with open('output/percipitation.csv', 'a') as csvFile:
    csvwriter = csv.writer(csvFile, delimiter=',')
    # input comes from STDIN
    for line in infile:
        properLine = re.search("^[A-Z]{3}-{1}[0-9]{7}.*:{1}-{1}.*", line)
        if properLine:
            # capture values from line
            file = line.rstrip()[:3]
            month = line.rstrip()[4:10]
            inches = line.rstrip()[18:]
            #inches = inches.decode('iso-8859-1').encode('utf8')
            try:
                if month == prevMonth:
                    count = float(inches) + count

                elif prevMonth == '':
                    print(inches)
                    count = 0
                    prevMonth = month
                    count = count + float(inches)

                elif month != prevMonth:
                    print(file, " - ", prevMonth, " : ", count)
                    csvwriter.writerow([file, prevMonth, count])
                    prevMonth = month
                    prevCount = count
                    count = 0.00

            except Exception as e:
                continue
                #print(e)

        else:
            continue

    print(file, " - ", prevMonth, " : ", prevCount)
    csvwriter.writerow([file, prevMonth, prevCount])
#csvwriter.close()
