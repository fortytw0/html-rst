import re
from tokenize import group

with open('data/sample_rst_tree.txt') as f : 
    tree = f.readlines()

tree = [t.strip() for t in tree]
doc_dic = {}

for t in tree : 

    
    if 'leaf' in t : 
        r1 = re.findall(r'\(leaf\s([0-9]*)\)' , t)
        r2 =  re.findall(r'\(text\s(.*)\s\)' , t)
        doc_dic[r1[0]] = r2[0][:-1]


print(doc_dic)


'''
Replace brackets in the text with -LB- and -RB-.
'''

with open('data/sample_rst_tree.txt') as f : 
    tree = f.readlines()

cleaned_tree = ''

regex = '\(.*text.*(\(.*\)).*\)'

for line in tree : 

    groups = re.findall(regex , line)

    if groups : 
        bracketed_text = groups[0]
        corrected_text = bracketed_text.replace('(' , '-LB-').replace(')' , '-RB-', 1)
        line = line.replace(bracketed_text, corrected_text)

    cleaned_tree += line


tokens = cleaned_tree.strip().replace('//TT_ERR','').replace('\n','').replace('(', ' ( ').replace(')', ' ) ').split()


'''
Parsing Attempt 1 : PyParsing with nestedExpr

DNW.
'''

# from pyparsing import nestedExpr

# print(nestedExpr('(' , ')').parseString(tokens))

'''
Parsing Attempt 2 : Creating own stack
'''

c = 0
parse = []
curr_parse = ''

for i , t in enumerate(tokens) : 
    
    if t=='(' : 
        c += 1
        

    elif t == ')' : 
        c -= 1
        parse.append(curr_parse)
        curr_parse = ''
    
    elif c == 0 :
        pass

    else : 
        curr_parse += t + ' '


cleaned_parse = []

for p in parse : 
    if 'prom' not in p : 
        cleaned_parse.append(p)


hparse = []
curr_hp = []
i = 0 

for i, cp in enumerate(cleaned_parse) : 

    if 'Root span' in cleaned_parse[i] : 
        curr_hp.append(cleaned_parse[i])

    elif 'Nucleus' in cleaned_parse[i] : 
        hparse.append(curr_hp)
        curr_hp = [cleaned_parse[i]]

    elif 'Satellite' in cleaned_parse[i] : 
        hparse.append(curr_hp)
        curr_hp = [cleaned_parse[i]]

    else : 
        curr_hp.append(cleaned_parse[i])


print(hparse)