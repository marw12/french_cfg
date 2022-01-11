# -*- coding: utf-8 -*-

# import libraries
import nltk
from nltk import Tree
import sys
import string
import re

# class respsonsible for converting CFG to CNF
class CNF_Converter():

    def __init__(self, rules, startingNonTerminal):
        self.rules = rules
        self.startingNonTerminal = startingNonTerminal
        self.terminal = {}
        self.temp_list = {}
        self.eliminateVariableUnit()
        self.moveTerminal()
        self.replaceLongNonTerminals()
        self.addStartingNonTerminal()

    def addStartingNonTerminal(self):
        for item in self.rules[self.startingNonTerminal]:
            if self.startingNonTerminal in item:
                prev_start = self.startingNonTerminal
                while self.startingNonTerminal in self.rules:
                    self.startingNonTerminal = self.startingNonTerminal+'0'
                self.rules[self.startingNonTerminal] = self.rules[prev_start]
            else:
                pass

    def createCombinations(self, element, nonterminal, count):
            numset = 1 << count
            new_prods = []

            for i in range(numset):
                nth_nt = 0
                new_prod = ''
                for s in element:
                    if s == nonterminal:
                        if i & (1 << nth_nt):
                            new_prod = new_prod+s
                        nth_nt += 1
                    else:
                        new_prod = new_prod+s
                new_prods.append(new_prod)
            return new_prods

    def moveTerminal(self):
        for key, value in self.rules.items():
            for i in range(len(value)):
                if re.compile(r'\'+\w+\'').search(value[i]) and any(c in value[i] for c in self.rules):
                    match = re.findall(r'\'+\w+\'', value[i])
                    for i in match:
                        self.terminal[i] = key
        for item, value in self.terminal.items():
            dict_new_nt = item.upper()
            dict_new_nt = dict_new_nt.replace("'","")
            while dict_new_nt in self.rules:
                dict_new_nt = self.getNewSymbol()
            self.rules[dict_new_nt] = [item]
            self.terminal[item] = dict_new_nt

    def eliminateVariableUnit(self):
        for key, value in self.rules.copy().items():
            flag=0
            for key2, value2 in self.rules.copy().items():
                if key in str(value2):
                    if key in value2 and key==key2:
                        self.rules[key].remove(key)
                    if key in value2:
                        self.rules[key2] = self.rules[key2] + self.rules[key]
                        self.rules[key2].remove(key)
                    for c in value2:
                        if key in c:
                            if key==c and flag!=2:
                                flag=1
                            else:
                                flag=2
                                break

            if flag==1 and key!=self.startingNonTerminal:
                self.rules.pop(key, None)


    def replaceLongNonTerminals(self):
        for key, value in self.rules.items():
            for i in range(len(value)):
                self.rules[key][i] = re.sub(' +',' ',value[i])

        for key, value in self.rules.copy().items():
            for key2, value2 in self.rules.copy().items():
                if key!=key2:
                    for i in range(len(value)):
                        for j in range(len(value2)):
                            if value2[j] in value[i] and len(value2)==1:
                                if len(value2[j].split(" "))!=2:
                                    self.rules[key][i]=self.rules[key][i].replace(value2[j], key2)
                               

        for key, value in self.rules.copy().items():
            for i in range(len(value)):
                if value[i] in self.rules:
                    if all( tkey.startswith("'") for tkey in self.rules[value[i]]):
                        self.rules[key][i] = self.rules[key][i].replace(value[i],self.rules[value[i]][0] )


        for key, value in self.rules.copy().items():
            for i in range(len(value)):
                splitted = value[i].split(" ")
                while len(self.rules[key][i].split(" "))>2:
                    item = self.getNewSymbol()
                    if self.rules[key][i].split(" ")[0]+" "+self.rules[key][i].split(" ")[1] not in self.temp_list:
                        self.temp_list[self.rules[key][i].split(" ")[0]+" "+self.rules[key][i].split(" ")[1]] = item
                    
                    self.rules[self.temp_list[self.rules[key][i].split(" ")[0]+" "+self.rules[key][i].split(" ")[1]]] = [self.rules[key][i].split(" ")[0]+" "+self.rules[key][i].split(" ")[1]]
                    self.rules[key][i] = self.rules[key][i].replace(self.rules[key][i].split(" ")[0]+" "+self.rules[key][i].split(" ")[1], self.temp_list[self.rules[key][i].split(" ")[0]+" "+self.rules[key][i].split(" ")[1]])

    def getNewSymbol(self):
        nt = list(string.ascii_uppercase)
        new_nt = ''
        for item in nt:
            if item in self.rules:
                continue
            else:
                new_nt = item
                break
        return new_nt

class CYK():
  
    def __init__(self, grammar_file, sentence):

        self.grammar_file = grammar_file
        self.words = [sentence]
        self.startSymbol = 'S'
        self.temp_table = []
        self.rules = {}
        self.read_grammar()
        self.converted = CNF_Converter(self.rules, self.startSymbol)

        for item in self.words:
            self.word = item
            self.read_output()
            self.parser()

    def read_grammar(self):

        f = open(self.grammar_file)
        self.startSymbol = f.readline().rstrip()

        for content in f:
            content = content.rstrip()
            rule = content.split(" -> ")

            if rule[0] not in self.rules:
                self.rules[rule[0]] = rule[1].split(" | ")
            else:
                self.rules[rule[0]] += (rule[1].split(" | "))


    def read_output(self):

        strng = ""

        for key, value in self.converted.rules.items():
            strng += str(key) + " -> "+ ' | '.join(map(str, value))+'\n'

        groucho_grammar = nltk.CFG.fromstring(strng)
        sent = self.word.split(" ")
        parser = nltk.ChartParser(groucho_grammar)
        print("Parse Trees:")
        tree = []

        for tree in parser.parse(sent):
          print(tree)
        

    def parser(self):

        self.table_copy = []
        tokenized_words = self.word.split(" ")
        size = len(tokenized_words)

        self.parse_table = [[[] for p in range(size - q)] for q in range(size)]

        for i, word in enumerate(tokenized_words):
            for key, value in self.converted.rules.items():
                for val in value:
                    if val == "'"+word+"'":
                        self.parse_table[0][i].append(key)
                        self.table_copy.append((key, val))

        for qualifying_words in range(2, size + 1):
            for current_cell in range(0, size - qualifying_words + 1):
                for left_side in range(1, qualifying_words):
                    right_side = qualifying_words - left_side

                    left_cell = self.parse_table[left_side - 1][current_cell]
                    right_cell = self.parse_table[right_side - 1][current_cell + left_side]

                    right_side = 0
                    left_side = 0
                    for key, value in self.converted.rules.items():
                        for item in value:
                            subitem = item.split(" ")
                            for left in left_cell:
                                if left == subitem[0]:
                                    left_side = 1
                                    for right in right_cell:
                                        if right == subitem[1]:
                                            right_side = 1
                                            if left_side == 1 and right_side == 1:
                                                self.parse_table[qualifying_words - 1][current_cell].append(key)
                                                self.table_copy.append((key, [subitem[0], subitem[1]], (left_side - 1, current_cell), (right_side - 1, current_cell + left_side), (qualifying_words - 1, current_cell) ))
                                        right_side = 0
                                        left_side = 0
        
    def find_tuple(self, tuples_list, value):

        val = []
        for t in tuples_list:
            if t[4] == value:
                val = t
                break

        return val

    def find(self, tuples_list, value):

        val = []
        for t in tuples_list:
            if t == value:
                val = t
                break

        return val

    def generate_tree(self, node):

        if isinstance(self.find(self.table_copy, node)[1], (list,)):
            item = self.find(self.table_copy, node)[1]
            item_x = self.find(self.table_copy, node)[2]
            item_y = self.find(self.table_copy, node)[3]

            if item_x[0]==0:
                x = self.table_copy_reversed[item_x[1]]
            else:
                x = self.find_tuple(self.table_copy, item_x)

            if item_y[0]==0:
                y = self.table_copy_reversed[item_y[1]]
            else:
                y = self.find_tuple(self.table_copy, item_y)

            return (node[0], self.generate_tree(x), self.generate_tree(y))
        else:
            return (node[0],  self.find(self.table_copy, node)[1])

if __name__ == "__main__":
    CYK("./french-grammar.txt", "le chat mange le poisson")
