import codecs
import sys
import os
import hashlib
import json
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
#Топологическая сортировка
def top_sort_children(key, tasks_n_deps, colors):
    res = []
    if (colors[key] == 2):
        return
    elif colors[key] == 1:
        raise BaseException
    else:
        colors[key] = 1
        for child in tasks_n_deps[key][0]:
            if child in tasks_n_deps:
                res += top_sort_children(child, tasks_n_deps, colors)
        colors[key] = 2
        res = [key] + res
        return res
def top_sort_tasks(tasks_n_deps):
    colors = {}
    res = []
    for task in list(tasks_n_deps.keys()):
        colors.update({task: 0})
    for task in list(colors.keys()):
        if (colors[task] == 2):
            continue
        elif colors[task] == 1:
            raise BaseException
        else:
            colors[task] = 1
            for child in tasks_n_deps[task][0]:
                if child in tasks_n_deps:
                    res += top_sort_children(child, tasks_n_deps, colors)
            colors[task] = 2
            res = [task] + res
    return res

#Файл для хэшей
MEMORY = 'make_memory.json'

#Чтение файла и парсинг
lexer = LangLexer()
parser = LangParser()
f = codecs.open(sys.argv[1], "r", "utf-8" )
data = f.read().strip()
if (len(data) > 0):
    tasks_n_deps = parser.parse(lexer.tokenize(data))
    #Создание отсортированного списка задач
    sorted_tasks = top_sort_tasks(tasks_n_deps)
    sorted_tasks.reverse()
    #Выполнение задач

    #База данных
    memory = {}
    changes = {}
    if os.path.exists(MEMORY):
        with open(MEMORY, 'r+', encoding='utf-8') as json_file:
            memory = json.load(json_file)
    #Выполняем задачи, начиная с самых основных
    for task in sorted_tasks:
        flag = False
        for file in tasks_n_deps[task][0]:
            #Выполняем условия
            if os.path.exists(file):
                if (file in memory):
                    with open(file, 'rb') as f:
                        hasher = hashlib.md5()
                        buf = f.read()
                        hasher.update(buf)
                        hash = hasher.hexdigest()
                        if (memory[file] != hash):
                            #Если файлы из условия поменялись, то записываем изменения
                            changes.update({file : hash})
                            flag = True
                else:
                    #Если файл из условия не записан в памяти
                    with open(file, 'rb') as f:
                        hasher = hashlib.md5()
                        buf = f.read()
                        hasher.update(buf)
                        hash = hasher.hexdigest()
                        changes.update({file : hash})
                    flag = True
            else:
                #При отсутствии требуемого файла получается ошибка
                raise FileNotFoundError
        #Если условия не были изменены, но цель удалена - выполняем команды
        flag |= not(os.path.exists(task))
        if flag:
            #Выполнение команд
            for command in tasks_n_deps[task][1]:
                os.system(command)
            #Обновление хэша цели
            with open(task, 'rb') as f:
                hasher = hashlib.md5()
                buf = f.read()
                hasher.update(buf)
                hash = hasher.hexdigest()
                changes.update({task : hash})
    memory.update(changes)
    with open(MEMORY, "w", encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)