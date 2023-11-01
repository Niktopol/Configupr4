import codecs
import sys
import os
from sly import Lexer, Parser
 
class LangLexer(Lexer):
    tokens = {COMMAND, COLON, LPAREN, RPAREN, LBRACE, RBRACE, TARGORCOND}

    ignore = ' \t'
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'

    TARGORCOND = r'\w+(\.[\w]+)?'
    COMMAND = r'\"[^\n]+\"'
    COLON = r':'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'

    @_(r'\w+(\.[\w]+)?')
    def COMMAND(self, t):
      t.value = t.value[1:-1]
      return t
class LangParser(Parser):
    tokens = LangLexer.tokens

    @_('block blocks')
    def blocks(self, p):
        tasks = dict()
        task = p.block
        tasks.update({task[0]:[task[1], task[2]]})
        tasks.update(p.blocks)
        return tasks
    @_('block')
    def blocks(self, p):
        tasks = dict()
        task = p.block
        tasks.update({task[0]:[task[1], task[2]]})
        return tasks

    @_('LPAREN TARGORCOND COLON RPAREN commands')
    def block(self, p):
        return [p.TARGORCOND, [], p.commands]
    
    @_('LPAREN TARGORCOND COLON conditions RPAREN commands')
    def block(self, p):
        return [p.TARGORCOND, p.conditions, p.commands]
    
    @_('TARGORCOND conditions')
    def conditions(self, p):
        return [p.TARGORCOND] + p.conditions

    @_('TARGORCOND')
    def conditions(self, p):
        return [p.TARGORCOND]

    @_('LBRACE cmd RBRACE')
    def commands(self, p):
        return p.cmd
    @_('LBRACE RBRACE')
    def commands(self, p):
        return []
    @_('COMMAND cmd')
    def cmd(self, p):
        return [p.COMMAND] + p.cmd
    @_('COMMAND')
    def cmd(self, p):
        return [p.COMMAND]

#Чтение файла и парсинг
lexer = LangLexer()
parser = LangParser()
f = codecs.open(sys.argv[1], "r", "utf-8" )
data = f.read().strip()
#Выполнение задач
if (len(data) > 0):
    tasks_n_deps = parser.parse(lexer.tokenize(data))
    main_tasks = []
    for task in list(tasks_n_deps.keys()):
        if(len(tasks_n_deps[task][1])) == 0:
            main_tasks.append(task)
    print(os.path.isfile(sys.argv[1]))

 

"""
class LangLexer(Lexer):
    tokens = {NAME, NUMBER, STRING, LPAREN, RPAREN, PLUS, FOR, ITER}
    ignore = ' \t\r'
    ignore_newline = r'\n+'
    ignore_comment = r'\#.*'
    NAME = r'[a-zA-z_][a-zA-Z0-9_]*'
    NUMBER = r'-?\d+(\.\d+)?'
    STRING = r'\"[^\"\']*\"'
    LPAREN = r'\('
    RPAREN = r'\)'
    PLUS = r'\+'
    NAME['FOR'] = FOR
    NAME['ITER'] = ITER
    @_(r'-?\d+(\.\d+)?')
    def NUMBER(self, t):
      if (float(t.value) > math.floor(float(t.value))):
          t.value = float(t.value)
      else:
          t.value = int(float(t.value))
      return t    
    @_(r'\"[^\"\']*\"')
    def STRING(self, t):
      t.value = t.value[1:-1]
      return t
    
class LangParser(Parser):
    tokens = LangLexer.tokens
    def __init__(self):
        self.iter = [0]
    def join_cycexpr(self, arr):
        f = False
        res = 0
        for i in arr:
            if (type(i) == str):
                f = True
                res = ''
                break
        for i in arr:
            if (f):
                res += str(i[0]) if type(i) == list else str(i)
            else:
                res += int(i[0]) if type(i) == list else i
        return res
    @_('LPAREN contents RPAREN')
    def object(self, p):
        return {key: value for key, value in p.contents}
    
    @_('value contents')
    def contents(self, p):
        return [p.value] + p.contents
    
    @_('NAME LPAREN expr RPAREN',
       'NAME LPAREN array RPAREN',
       'NAME LPAREN object RPAREN')
    def value(self, p):
        return p.NAME, p[2]

    @_('')
    def contents(self, p):
        return []
    
    @_('NUMBER',
       'STRING')
    def expr(self, p):
        return p[0]
    
    @_('NUMBER PLUS expr',
       'STRING PLUS expr')
    def expr(self, p):
        try:
            return p[0]+p.expr
        except TypeError:
            return str(p[0])+str(p.expr)
        
    @_('ITER')
    def cycexpr(self, p):
        return [self.iter]

    @_('NUMBER',
       'STRING')
    def cycexpr(self, p):
        return p[0]
    
    @_('ITER PLUS cycexpr')
    def cycexpr(self, p):
        tmp = [self.iter]
        tmp.extend(p.cycexpr)
        return tmp
    
    @_('NUMBER PLUS cycexpr',
       'STRING PLUS cycexpr')
    def cycexpr(self, p):
        tmp = [p[0]]
        tmp.extend(p.cycexpr)
        return tmp
        
    @_('expr',
       'object')
    def item(self, p):
        return [p[0]]
    
    @_('expr item',
       'object item')
    def item(self, p):
        tmp = [p[0]]
        tmp.extend(p.item)
        return tmp
    
    @_('expr item',
       'object item')
    def array(self, p):
        tmp = [p[0]]
        tmp.extend(p.item)
        return tmp
    
    @_('FOR LPAREN NUMBER NUMBER RPAREN LPAREN cycexpr RPAREN')
    def array(self, p):
        arr = []
        res = p.cycexpr
        for i in range(p[2], p[3]):
            self.iter[0] = i
            arr.append(self.join_cycexpr(res))
        return arr
    
data = '''(x(FOR(1 10)(ITER)))'''
lexer = LangLexer()
parser = LangParser()
#f = codecs.open(sys.argv[1], "r", "utf-8" )
#data = f.read()
print(json.dumps(parser.parse(lexer.tokenize(data)), ensure_ascii=False, indent=2))
 
"""