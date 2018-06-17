#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import pandas as pd
import re

def replace_line(pat,text,lines,color):
    if color:
        text = 'style="color:green"|' + text

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
            replace_line(pat,dat['GRP'][x][y],lines,False)
            
    #teens
    for x in range(8):
        for y in range(2):
            pat = '{T' + str(x) + str(y) + '}'
            if dat['STN'][x][y] == dat['QFS'][x/2][x%2]:
                color = True
            else:
                color = False                
            replace_line(pat,dat['STN'][x][y],lines,color)
        
    #QFs
    for x in range(4):
        for y in range(2):
            pat = '{Q' + str(x) + str(y) + '}'
            if dat['QFS'][x][y] == dat['SFS'][x/2][x%2]:
                color = True
            else:
                color = False                
            replace_line(pat,dat['QFS'][x][y],lines,color)

    #SFs
    for x in range(2):
        for y in range(2):
            pat = '{S' + str(x) + str(y) + '}'
            if dat['SFS'][x][y] == dat['F'][x]:
                color = True
            else:
                color = False
            replace_line(pat,dat['SFS'][x][y],lines,color)
        
    #Fs
    pat = '{F00}'
    replace_line(pat,dat['F'][0],lines,(dat['F'][0]==dat['W'])) 
    pat = '{F01}'   
    replace_line(pat,dat['F'][1],lines,(dat['F'][1]==dat['W']))
    
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


def print_header():
    print '__NOTOC__\n'\
        '===Bracket Challenge===\n'\
        'Welcome to Cavium’s World Cup Bracket Challenge!\n'\
        '<br>We have 24 people who signed up with the fee, so the prizes are going to be:\n'\
        '*1st place: $120\n'\
        '*2nd place: $60\n'\
        '*3rd place: $40\n'\
        '*last place: $20\n\n'\
        'Good Luck with your brackets and Enjoy World Cup!!! J\n\n'\
        '===Scoring===\n'\
        'Group Stage Scoring\n'\
        '*Correctly predict a Group winner: 10 points\n'\
        '*Correctly predict a Group Runner-Up: 10 points\n'\
        '*Correctly predict the top two teams (in any order): 3 points\n'\
        '*Correctly predict the entire group in the correct order: 15 points\n\n'\
        'Knockout Stage Scoring\n'\
        '*For each correct team in the Quarter-Finals: 3 points\n'\
        '*For each correct team in the Semi-Finals: 4 points\n'\
        '*For each correct team in the Final: 5 points\n'\
        '*For the correct World Cup 2018 Winner: 10 points\n'\
        '*For the correct World Cup 2018 Runner-up: 8 points\n'\
        '*Correctly predict a fixture (both correct teams and the correct position in the bracket): 10 points\n\n'\
        '===Scoring Table===\n'\
        '{| class="wikitable sortable" style="text-align:left; border: 1px solid darkgray;"\n'\
        '! Name\n'\
        '! Score\n'\
        '|-\n'

    for sheet in xx.sheet_names:        
        print '| [[2018FIFA#' + sheet + ' | ' + sheet + ']] || 0'
        print '|-'
    print '|}'
        
    

if __name__ == '__main__':
    
    xx = pd.ExcelFile("brack.xlsx")

    print_header()
    
    for sheet in xx.sheet_names:
        sh = xx.parse(sheet)
        dat = xtract_sheet(sh)
        print_table(sheet,dat)
