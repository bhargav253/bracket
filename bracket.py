#!/usr/bin/python2.7

import pandas as pd
import re

def replace_line(pat,text,lines):
    for l in range(len(lines)):
        m = re.sub(pat,text,lines[l])
        if m:
            lines[l] = m
    

def print_table(sheet,dat):
    temp_file = open('template','r')
    ls = temp_file.readlines()
    lines = []
    for l in ls:
        m = re.sub('{Name}',sheet,l)
        if m:
            lines.append(m)
        else:
            lines.append(l)

    #groups
    for x in range(8):
        for y in range(4):            
            pat = '{G' + str(x) + str(y) + '}'
            replace_line(pat,dat['GRP'][x][y],lines)
            
    #teens
    for x in range(8):
        for y in range(2):
            pat = '{T' + str(x) + str(y) + '}'
            replace_line(pat,dat['STN'][x][y],lines)
        
    #QFs
    for x in range(4):
        for y in range(2):
            pat = '{Q' + str(x) + str(y) + '}'
            replace_line(pat,dat['QFS'][x][y],lines)

    #SFs
    for x in range(2):
        for y in range(2):
            pat = '{S' + str(x) + str(y) + '}'
            replace_line(pat,dat['SFS'][x][y],lines)
        
    #Fs
    pat = '{F00}'
    replace_line(pat,dat['F'][0],lines) 
    pat = '{F01}'   
    replace_line(pat,dat['F'][1],lines)
    
    for l in lines:
        print l

    temp_file.close()
        
def xtract_sheet(sheet):
    g = []
    t = []
    q = []
    s = []
    f = []

    #groups
    for x in range(8):
        grp = []
        grp.append(sheet.iloc[(5*x)+2][2])
        grp.append(sheet.iloc[(5*x)+3][2])
        grp.append(sheet.iloc[(5*x)+4][2])
        grp.append(sheet.iloc[(5*x)+5][2])        

        g.append(grp)

    #for e in g:
    #    print e

    #teens
    for x in range(8):
        grp = []
        grp.append(sheet.iloc[(3*x)+2][4])
        grp.append(sheet.iloc[(3*x)+3][4])

        t.append(grp)

    #for e in t:
    #    print e

    #QFs
    for x in range(4):
        grp = []
        grp.append(sheet.iloc[(6*x)+4][7])
        grp.append(sheet.iloc[(6*x)+5][7])

        q.append(grp)

    #for e in q:
    #    print e

    #SFs
    for x in range(2):
        grp = []
        grp.append(sheet.iloc[(12*x)+7][10])
        grp.append(sheet.iloc[(12*x)+8][10])

        s.append(grp)

    #for e in s:
    #    print e
        
    #Fs
    f.append(sheet.iloc[12][13])
    f.append(sheet.iloc[13][13])    

    #print f

    w = sheet.iloc[13][14]

    #print w

    dat = { 'GRP' : g,
            'STN' : t,
            'QFS' : q,
            'SFS' : s,
            'F'   : f,
            'W'   : w}

    return dat


if __name__ == '__main__':
    
    xx = pd.ExcelFile("brack.xlsx")

    print '===Scoring Table==='
    print '{| class="wikitable sortable" style="text-align:left; border: 1px solid darkgray;"'
    print '! Name'
    print '! Score'
    print '|-'
    for sheet in xx.sheet_names:        
        print '| [[2018FIFA#' + sheet + ' | ' + sheet + ']] || 0'
        print '|-'
    print '|}'
        
    for sheet in xx.sheet_names:
        sh = xx.parse(sheet)
        dat = xtract_sheet(sh)
        print_table(sheet,dat)
