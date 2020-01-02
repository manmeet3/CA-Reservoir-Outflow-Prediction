#!/usr/bin/env python

from operator import itemgetter
import sys
import re
import csv



# Month Average
file= ''
prevMonth = ''
count = 0.00 # total value in inches -- total amount of snow in a given month
prevCount = 0.00

infile = sys.stdin

with open('output/snow.csv', 'a') as csvFile:
    csvwriter = csv.writer(csvFile, delimiter=',')
    # input comes from STDIN
    for line in infile:
        properLine = re.search("^[A-Z]{3}-{1}[0-9]{7}.*:{1}-{1}.*", line)
        if properLine:
            # capture values from line
            file = line.rstrip()[:3] # sensor name
            month = line.rstrip()[4:10] # month + year
            inches = line.rstrip()[18:]
            #inches = inches.decode('iso-8859-1').encode('utf8')
            try:
                if month == prevMonth: # for a given month, when a subsequent day comes up. keep adding to same month
                    count = float(inches)

                elif prevMonth == '':
                    print(inches)
                    count = 0
                    prevMonth = month
                    count = float(inches) # first iteration stores first day in count

                elif month != prevMonth:
                    # save current count into prevMonth
                    print(file, " - ", prevMonth, " : ", count)
                    #amount = count/30
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
    amount = prevCount/30
    csvwriter.writerow([file, prevMonth, prevCount])
#csvwriter.close()
