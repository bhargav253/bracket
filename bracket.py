#!/usr/bin/python2.7

import pandas as pd
import re

def replace_line(pat,text,lines):
    for l in range(len(lines)):
        m = re.search(pat,lines[l])
        if m:
            lines[l] = m.group(1) + text + m.group(2)
    

def print_table(sheet,dat):
    temp_file = open('template','r')
    ls = temp_file.readlines()
    lines = []
    for l in ls:
        m = re.search('(.*?){Name}(.*)',l)
        if m:
            lines.append(m.group(1) + sheet + m.group(2))
        else:
            lines.append(l)

    #groups
    for x in range(8):
        pat = '(.*?){G' + str(x) + '0}(.*)'
        replace_line(pat,dat['GRP'][x][0],lines)

        pat = '(.*?){G' + str(x) + '1}(.*)'
        replace_line(pat,dat['GRP'][x][1],lines)

        pat = '(.*?){G' + str(x) + '2}(.*)'
        replace_line(pat,dat['GRP'][x][2],lines)

        pat = '(.*?){G' + str(x) + '3}(.*)'
        replace_line(pat,dat['GRP'][x][3],lines)
        
    #teens
    for x in range(8):
        pat = '(.*?){T' + str(x) + '0}(.*)'
        replace_line(pat,dat['STN'][x][0],lines)

        pat = '(.*?){T' + str(x) + '1}(.*)'
        replace_line(pat,dat['STN'][x][1],lines)
        
    #QFs
    for x in range(4):
        pat = '(.*?){Q' + str(x) + '0}(.*)'
        replace_line(pat,dat['QFS'][x][0],lines)

        pat = '(.*?){Q' + str(x) + '1}(.*)'
        replace_line(pat,dat['QFS'][x][1],lines)

    #SFs
    for x in range(2):
        pat = '(.*?){S' + str(x) + '0}(.*)'
        replace_line(pat,dat['SFS'][x][0],lines)

        pat = '(.*?){S' + str(x) + '1}(.*)'
        replace_line(pat,dat['SFS'][x][1],lines)
        
    #Fs
    pat = '(.*?){F00}(.*)'
    replace_line(pat,dat['F'][0],lines) 
    pat = '(.*?){F11}(.*)'   
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
