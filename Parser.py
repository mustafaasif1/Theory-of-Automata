import Lexer

import ply.lex as lex
import ply.yacc as yacc
import sys
import os


precedence = (
    ('nonassoc', 'LESSTHAN', 'GREATERTHAN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

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

def p_whole_code(p):
    '''
    whole_code    : full_code
    '''
    p[0] = p[1]
    # eval_all_code(p[0])
    # print(p[0])

def p_full_code(p):
    '''
    full_code    : if_block full_code
                | statement full_code
                | make_struct full_code
                | initialize_struct full_code
                | assign_struct full_code
    '''
    p[0] = (p[1], p[2])
    # eval_all_statement(p[1])

def p_full_code2(p):
    '''
    full_code    :
    '''
    p[0] = 'empty'


def p_initialize_struct(p):
    '''
    initialize_struct    : STRING STRING
    '''
    p[0] = ('initialize_struct', p[1], p[2])


def p_make_struct(p):
    '''
    make_struct    : STRUCT STRING LBRACE all_types RBRACE SEMI
    '''
    p[0] = (p[1], p[2], p[4])


def p_assign_struct(p):
    '''
    assign_struct    : STRING DOT STRING EQUALS expression
    '''
    p[0] = ('assign_struct', p[1], p[3], p[4], p[5])




def p_all_types_empty(p):
    '''
    all_types    :
    '''
    p[0] = 'last'


def p_all_types(p):
    '''
    all_types : DEFINT expression all_types
                                    | DEFDOUBLE expression all_types
                                    | DEFSTRING expression all_types
                                    | DEFCHAR expression all_types
                                    | DEFBOOL expression all_types
    '''
    p[0] = (p[1], p[2], p[3])


def p_if_block(p):
    '''
    if_block    : IF LPAREN expression RPAREN LBRACE statement RBRACE elseif_else_block
                | IF LPAREN expression RPAREN LBRACE if_block RBRACE elseif_else_block
    '''
    p[0] = (p[1], p[3], p[6], p[8])
    # print(p[0])
    # print(eval_if_else_statment(p[0])


def p_elseif_else_block_else(p):
    '''
    elseif_else_block   : ELSE LBRACE statement RBRACE
                        | ELSE LBRACE if_block RBRACE
    '''

    p[0] = (p[1], True , p[3], 'empty')

def p_elseif_else_block_notempty(p):
    '''
    elseif_else_block   : ELSEIF LPAREN expression RPAREN LBRACE statement RBRACE elseif_else_block
                        | ELSEIF LPAREN expression RPAREN LBRACE if_block RBRACE elseif_else_block
    '''
    p[0] = (p[1], p[3], p[6], p[8])


def p_elseif_else_block_empty(p):
    '''
    elseif_else_block : 
    '''
    p[0] = 'empty'


def p_statement(p):
    '''
    statement : expression
            | type_var_assign
            | empty
            | print_statement
            | increment_decrement
    '''
    p[0] = p[1]
    # print(eval_assignment_and_print(p[1]))    


def p_increment_decrement(p):
    '''
    increment_decrement 	: expression INCREMENT
                                                        | expression DECREMENT
    '''

    p[0] = (p[2], p[1])





def p_print_statement(p):
    '''
    print_statement 	: PRINT LPAREN INT insidepart RPAREN
                                            | PRINT LPAREN bool insidepart RPAREN
                                            | PRINT LPAREN DOUBLE insidepart RPAREN
    '''

    p[0] = ('print', 'type', p[3], p[4])

def p_print_statement2(p):
    '''
    print_statement     : PRINT LPAREN FINDSTRING insidepart RPAREN
    '''

    p[0] = ('print', 'str', p[3], p[4])

def p_print_statement3(p):
    '''
    print_statement     : PRINT LPAREN expression insidepart RPAREN
    '''

    p[0] = ('print', 'exp', p[3], p[4])


def p_print_statement4(p):
    '''
    print_statement     : PRINT LPAREN STRING DOT STRING insidepart RPAREN
    '''

    p[0] = ('print', 'struct',(p[3], p[5]), p[6])



def p_insidepart1(p):
    '''
    insidepart 	: COMMA INT insidepart
                            | COMMA bool insidepart
                            | COMMA DOUBLE insidepart
    '''

    p[0] = ('print', 'type', p[2], p[3])


def p_insidepart2(p):
    '''
    insidepart  : COMMA FINDSTRING insidepart
    '''

    p[0] = ('print', 'str', p[2], p[3])

def p_insidepart3(p):
    '''
    insidepart  : COMMA expression insidepart
    '''

    p[0] = ('print', 'exp', p[2], p[3])

def p_insidepart4(p):
    '''
    insidepart  : COMMA STRING DOT STRING insidepart
    '''

    p[0] = ('print', 'struct', (p[2], p[4]), p[5])


def p_bool(p):
    '''
    bool 	: TRUE
                    | FALSE
    '''
    p[0] = p[1]


def p_end_string(p):
    '''
    insidepart 	:
    '''
    p[0] = 'last'

def p_expression_negation_without_brackets(p):
    '''
    expression  : NOT expression
    '''
    p[0] = (p[1], p[2])


def p_expression_negation(p):
    '''
    expression  : LPAREN NOT expression RPAREN
    '''
    p[0] = (p[2], p[3])



def p_expression_operation(p):
    '''
    expression : LPAREN expression AND expression RPAREN
               | LPAREN expression OR expression RPAREN
               | LPAREN expression DOUBLEEQUAL expression RPAREN
               | LPAREN expression NOTEQUAL expression RPAREN
               | LPAREN expression GREATERTHANEQUAL expression RPAREN
               | LPAREN expression LESSTHANEQUAL expression RPAREN
               | LPAREN expression GREATERTHAN expression RPAREN
               | LPAREN expression LESSTHAN expression RPAREN

    '''
    p[0] = (p[3], p[2], p[4])


def p_boolean_aglebra(p):
    '''
    expression 	: expression LESSTHAN expression
                                            | expression GREATERTHAN expression
                                            | expression LESSTHANEQUAL expression
                                            | expression GREATERTHANEQUAL expression
                                            | expression NOTEQUAL expression
                                            | expression DOUBLEEQUAL expression
                                            | expression AND expression
                                            | expression OR expression
    '''
    p[0] = (p[2], p[1], p[3])


def p_type_var_assign(p):
    '''
    type_var_assign : DEFINT var_assign
                                    | DEFDOUBLE var_assign
                                    | DEFSTRING var_assign
                                    | DEFCHAR var_assign
                                    | DEFBOOL var_assign
    '''
    p[0] = (p[1], p[2])


def p_var_assign_without_number(p):
    '''
    var_assign 	: STRING
                            | CHAR

    '''

    p[0] = ('=', p[1], 0)


def p_var_assign(p):
    '''
    var_assign 	: STRING EQUALS expression
                            | CHAR EQUALS expression

    '''

    p[0] = ('=', p[1], p[3])


def p_expression(p):
    '''
    expression 	: expression MULTIPLY expression
                            | expression DIVIDE expression
                            | expression PLUS expression
                            | expression MINUS expression
                            | expression POWER expression
                            | expression MODULUS expression
    '''
    p[0] = (p[2], p[1], p[3])


def p_expression_removing_brackets(p):
    '''
    expression 	: LPAREN expression RPAREN

    '''
    p[0] = p[2]


def p_expression_find_string(p):
    '''
    expression 	: FINDSTRING
                            | FINDCHAR

    '''
    p[0] = p[1]


def p_expression_int_float_bool(p):
    '''
    expression 	: INT
                            | DOUBLE
                            | TRUE
                            | FALSE
    '''
    p[0] = p[1]


def p_expression_var(p):
    '''
    expression 	: STRING
                            | CHAR
    '''
    p[0] = ("var", p[1])


def p_error(p):
    '''
    empty	:
    '''
    p[0] = None


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


lexer1 = Lexer.lexer
parser1 = yacc.yacc()