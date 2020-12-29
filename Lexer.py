import ply.lex as lex
import ply.yacc as yacc
import sys
import os

tokens = [
    'INT',  # Done
    'DOUBLE',  # Done
    'CHAR',  # Done
    'STRING',  # Done
    'TRUE',  # Done
    'FALSE',  # Done

    'EQUALS',  # Done

    'PLUS',  # Done
    'MINUS',  # Done
    'DIVIDE',  # Done
    'MULTIPLY',  # Done
    'POWER',  # Done
    'MODULUS',  # Done
    'INCREMENT',  # Done
    'DECREMENT',  # Done

    'LESSTHAN',  # Done
    'GREATERTHAN',  # Done
    'LESSTHANEQUAL',  # Done
    'GREATERTHANEQUAL',  # Done
    'NOTEQUAL',  # Done
    'DOUBLEEQUAL',  # Done
    'NOT',  # Done
    'AND',  # Done
    'OR',  # Done

    'SEMI',  # Done
    'LBRACE',  # Done
    'RBRACE',  # Done

    'LPAREN',  # Done
    'RPAREN',  # Done

    'PRINT',  # Done
    'IF',  # Done
    'ELSEIF',  # Done
    'ELSE',  # Done

    'DEFINT',
    'DEFDOUBLE',
    'DEFCHAR',
    'DEFSTRING',
    'DEFBOOL',

    'FINDSTRING',
    'FINDCHAR',
    'COMMA',

    'STRUCT',
    'DOT',

]

states = (('eolcomment', 'exclusive'),  ('delimitedcomment', 'exclusive'), )


def t_eolcomment(t):
    r'//'
    t.lexer.begin('eolcomment')


def t_eolcomment_end(t):
    r'\n'
    t.lexer.begin('INITIAL')


def t_delimitedcomment(t):
    r'/\*'
    t.lexer.begin('delimitedcomment')


def t_delimitedcomment_end(t):
    r'\*/'
    t.lexer.begin('INITIAL')


t_delimitedcomment_ignore = r'.'
t_eolcomment_ignore = r'.'


def t_eolcomment_error(t):
    t.lexer.skip(1)


def t_delimitedcomment_error(t):
    t.lexer.skip(1)


t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_POWER = r'\^'
t_MODULUS = r'\%'
t_EQUALS = r'\='
t_INCREMENT = r'\+\+'
t_DECREMENT = r'\-\-'

t_LESSTHAN = r'\<'
t_GREATERTHAN = r'\>'


t_NOT = r'\!'
t_AND = r'\&'
t_OR = r'\|'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r'\,'
t_DOT = r'\.'

t_ignore = ' \t\v\r'


def t_LESSTHANEQUAL(t):
    r'<='
    return t


def t_GREATERTHANEQUAL(t):
    r'>='
    return t


def t_NOTEQUAL(t):
    r'!='
    return t


def t_DOUBLEEQUAL(t):
    r'=='
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSEIF(t):
    r'elseif'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_PRINT(t):
    r'print'
    return t


def t_DEFINT(t):
    r'int'
    return t


def t_DEFDOUBLE(t):
    r'double'
    return t


def t_DEFCHAR(t):
    r'char'
    return t


def t_DEFSTRING(t):
    r'string'
    return t


def t_DEFBOOL(t):
    r'bool'
    return t

def t_STRUCT(t):
    r'struct'
    return t


def t_DOUBLE(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_TRUE(t):
    r'(true)'
    t.value = True
    return t


def t_FALSE(t):
    r'(false)'
    t.value = False
    return t


def t_STRING(t):
    r'[a-zA-Z][a-zA-Z_0-9]+'
    t.type = 'STRING'
    return t


def t_CHAR(t):
    r'[a-zA-Z]'
    t.type = 'CHAR'
    return t


def t_LBRACE(t):
    r'{'
    return t


def t_RBRACE(t):
    r'}'
    return t


def t_SEMI(t):
    r';'
    return t


def t_FINDSTRING(t):
    r'"(.*?)"'
    t.value = t.value[1:-1]
    return t


def t_FINDCHAR(t):
    r"'[a-zA-Z]'"
    t.value = t.value[1:-1]
    return t


def t_error(t):
    print("Illegal character '{0}' at line {1}".format(t.value[0], t.lineno))
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


lexer = lex.lex()