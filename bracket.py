#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import pandas as pd
import re

def group_chk(dat,x):
    score = 0
    #winner check
    if dat[x][0] == winner['GRP'][x][0]:
        score = score + 10
    if dat[x][1] == winner['GRP'][x][1]:
        score = score + 10

    top_two = ((dat[x][0] == winner['GRP'][x][0]) & (dat[x][1] == winner['GRP'][x][1])) | \
              ((dat[x][0] == winner['GRP'][x][1])  & (dat[x][1] == winner['GRP'][x][0]))              

    if top_two:
        score = score + 3

    order = 1    
    for y in range(4):
        if dat[x][y] != winner['GRP'][x][y]:        
            order = order & 0

    if order:
        score = score + 15

    return score
        

def replace_line(pat,text,lines,wpat,win):
    for l in range(len(lines)):
        m = re.sub(pat,text,lines[l])
        if m:
            lines[l] = m

        if wpat:
            if win:
                m = re.sub(wpat,'W',lines[l])
                if m:
                    lines[l] = m                    
            else:
                m = re.sub(wpat,'',lines[l])            
                if m:
                    lines[l] = m                    


            
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

    if f[0] == w:
        r = f[1]
    else:
        r = f[0]
    
    #print w

    dat = { 'GRP' : g,
            'STN' : t,
            'QFS' : q,
            'SFS' : s,
            'F'   : f,
            'W'   : w,
            'R'   : r }

    return dat


def load_lines(sheet):
    temp_file = open('template','r')
    ls = temp_file.read()
    ls = ls.splitlines()
    lines = []
    for l in ls:
        m = re.sub('{Name}',sheet,l)
        if m:
            lines.append(m)
        else:
            lines.append(l)

    temp_file.close()
            
    return lines

def make_table(lines,dat):
    #groups
    for x in range(8):
        for y in range(4):            
            pat = '{G' + str(x) + str(y) + '}'
            replace_line(pat,dat['GRP'][x][y],lines,None,None)
            
    #teens
    for x in range(8):
        for y in range(2):
            pat = '{T' + str(x) + str(y) + '}'
            wpat = '{TW' + str(x) + str(y) + '}'            
            if dat['STN'][x][y] == dat['QFS'][x/2][x%2]:
                win = True
            else:
                win = False                
            replace_line(pat,dat['STN'][x][y],lines,wpat,win)
        
    #QFs
    for x in range(4):
        for y in range(2):
            pat = '{Q' + str(x) + str(y) + '}'
            wpat = '{QW' + str(x) + str(y) + '}'            
            if dat['QFS'][x][y] == dat['SFS'][x/2][x%2]:
                win = True
            else:
                win = False                
            replace_line(pat,dat['QFS'][x][y],lines,wpat,win)

    #SFs
    for x in range(2):
        for y in range(2):
            pat = '{S' + str(x) + str(y) + '}'
            wpat = '{SW' + str(x) + str(y) + '}'            
            if dat['SFS'][x][y] == dat['F'][x]:
                win = True
            else:
                win = False
            replace_line(pat,dat['SFS'][x][y],lines,wpat,win)
        
    #Fs
    pat  = '{F00}'
    wpat = '{FW00}'    
    replace_line(pat,dat['F'][0],lines,wpat,(dat['F'][0]==dat['W'])) 
    pat  = '{F11}'
    wpat = '{FW11}'       
    replace_line(pat,dat['F'][1],lines,wpat,(dat['F'][1]==dat['W']))


def evaluate_score(lines,dat):
    tot_score = 0

    #groups
    for x in range(8):
        score = group_chk(dat['GRP'],x)
        pat = '{GP' + str(x) + '}'
        replace_line(pat,str(score),lines,None,None)
        tot_score = tot_score + score

    #teens brackets
    for x in range(8):
        brack = (dat['STN'][x][0] == winner['STN'][x][0]) & \
                (dat['STN'][x][1] == winner['STN'][x][1])
        if brack:
            score = 10
        else:
            score = 0

        pat = '{TP' + str(x) + '}'
        replace_line(pat,str(score),lines,None,None)
        tot_score = tot_score + score        

    #QFs
    for x in range(4):
        brack = (dat['QFS'][x][0] == winner['QFS'][x][0]) & \
                (dat['QFS'][x][1] == winner['QFS'][x][1])
        if brack:
            score = 10
        else:
            score = 0

        for ele in winner['QFS']:
            if (dat['QFS'][x][0] in ele):
                score = score + 3
            if(dat['QFS'][x][1] in ele):
                score = score + 3                        
            
        pat = '{QP' + str(x) + '}'
        replace_line(pat,str(score),lines,None,None)
        tot_score = tot_score + score        
        
    #SFs
    for x in range(2):

        brack = (dat['SFS'][x][0] == winner['SFS'][x][0]) & \
                (dat['SFS'][x][1] == winner['SFS'][x][1])
        if brack:
            score = 10
        else:
            score = 0

        for ele in winner['SFS']:
            if (dat['SFS'][x][0] in ele):
                score = score + 4
            if(dat['SFS'][x][1] in ele):
                score = score + 4                
            
        pat = '{SP' + str(x) + '}'
        replace_line(pat,str(score),lines,None,None)
        tot_score = tot_score + score        
        

    #final bracket
    brack = (dat['F'][0] == winner['F'][0]) & \
            (dat['F'][1] == winner['F'][1])
    if brack:
        score = 10
    else:
        score = 0

    score = 5 * len(list(set(dat['F']).intersection(winner['F'])))
    if dat['W'] == winner['W']:
        score = score + 10
    elif dat['R'] == winner['R']:
        score = score + 8
    
    pat = '{FP0}'
    replace_line(pat,str(score),lines,None,None)
    tot_score = tot_score + score    

    return tot_score

    
def print_header():
    print '__NOTOC__\n'\
        '===Bracket Challenge===\n'\
        'Welcome to Cavium’s World Cup Bracket Challenge!\n'\
        'Good Luck with your brackets and Enjoy World Cup!!! J\n\n'\
        '[[File:Bracket.xlsx]]'\
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

    for key in sheet_score:        
        print '| [[2018FIFA#' + key + ' | ' + key + ']] || ' + str(sheet_score[key])
        print '|-'
    print '|}'
        

def add_lines(lines):

    for l in lines:
        _out.append(l)
               

if __name__ == '__main__':
    
    xx = pd.ExcelFile("brack.xlsx")

    global winner
    global _out
    global sheet_score    

    sheet_score = {}
    _out = []
    
    for sheet in xx.sheet_names:
        if sheet == 'winner':
            sh = xx.parse(sheet)
            winner = xtract_sheet(sh)
        else:
            sh = xx.parse(sheet)
            dat = xtract_sheet(sh)
            lines = load_lines(sheet)
            make_table(lines,dat)
            sheet_score[sheet] = evaluate_score(lines,dat)
            add_lines(lines)

    print_header()            

    for l in _out:
        print l
    
