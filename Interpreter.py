import Parser
import Lexer

import ply.lex as lex
import ply.yacc as yacc
import sys
import os

env = {}
structs = {}
temp = {}

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


def eval_adding_struct_values(p):
    global temp

    if p[2] == 'last':
        if p[0] == 'bool':
            temp[p[1][1]] = ('bool', True)
        elif p[0] == 'int':
            temp[p[1][1]] = ('int', 0)
        elif p[0] == 'double':
            temp[p[1][1]] = ('double', 0.0)
        elif p[0] == 'string':
            temp[p[1][1]] = ('string', "")
        return
    else:
        if p[0] == 'bool':
            temp[p[1][1]] = ('bool', True)
        elif p[0] == 'int':
            temp[p[1][1]] = ('int', 0)
        elif p[0] == 'double':
            temp[p[1][1]] = ('double', 0.0)
        elif p[0] == 'string':
            temp[p[1][1]] = ('string', "")
        return eval_adding_struct_values(p[2])

    
def eval_all_code(p):
    global env
    global temp
    global structs

    first = p[0]
    second = p[1]

    if second == 'empty':
        eval_all_statement(first)
        return
    else:
        eval_all_statement(first)
        return eval_all_code(p[1])
        
        

        
def eval_all_statement(p):
    global env
    global temp
    global structs

    if p[0] == 'assign_struct':
        # print('assign_struct')
        if p[1] in env:
            if p[2] in env[p[1]]:
                temp_dict = env[p[1]].copy()
                if type(p[4]) == bool:
                    temp_dict[p[2]] = ('bool',p[4])
                elif type(p[4]) == str:
                    temp_dict[p[2]] = ('string',p[4])
                elif type(p[4]) == float:
                    temp_dict[p[2]] = ('double',p[4])
                elif type(p[4]) == int:
                    temp_dict[p[2]] = ('int',p[4])
                # print(temp_dict)
                env[p[1]] = temp_dict
                # print(env)
            else:
                print("This struct does not have this attribute")

        else:
            print('This struct does not exist')


    elif p[0] == 'struct':
        # print('struct')
        eval_adding_struct_values(p[2])
        structs[p[1]] = temp
        temp = {}
        # print(structs)
        # All the structs have been stored

    elif p[0] == 'initialize_struct':
        # print('init')
        if p[1] in structs:
            env[p[2]] = structs[p[1]]
            # print(env)
        else:
            print('This stuct does not exist')
        # This is also correct

    elif p[0] == 'if':
        value = eval_boolean_logic(p[1])
        if value == True:
            eval_all_statement(p[2])
        else:
            if p[3] == 'empty':
                return
            else:
                eval_all_statement(p[3])
    elif p[0] == 'elseif':
        value = eval_boolean_logic(p[1])
        if value == True:
            eval_all_statement(p[2])
        else:
            if p[3] == 'empty':
                return
            else:
                eval_all_statement(p[3])
    elif p[0] == 'else':
        value = eval_boolean_logic(p[1])
        if value == True:
            eval_all_statement(p[2])
        else:
            if p[3] == 'empty':
                return
            else:
                eval_all_statement(p[3])
    else:
        eval_assignment_and_print(p)
    

def eval_assignment_and_print(p):
    global env
    if p[0] == 'print':
        value = eval_print(p)
        if value == 'TypeError':
            print(value)
            exit(1)
        else:
            print(value)
    elif p[0] == "++" or p[0] == "--":
        return eval_increment_decrement(p)
    else:
        return eval_assignment(p)


def eval_increment_decrement(p):
    global env

    if p[1][1] in env:
        if p[0] == "++":
            temp_tuple = env[p[1][1]]
            value1 = temp_tuple[1] + 1
            type1 = temp_tuple[0]
            newtuple = (type1, value1)
            env[p[1][1]] = newtuple
            # print(env)

        elif p[0] == "--":
            temp_tuple = env[p[1][1]]
            value1 = temp_tuple[1] - 1
            type1 = temp_tuple[0]
            newtuple = (type1, value1)
            env[p[1][1]] = newtuple
            # print(env)
    else:
        return 'Variable doesnot exist'


def find_value_variable_in_environment(p):
    global env

    try:
        if type(p) == tuple:
            if p[1] in env:
                return str(env[p[1]][1])
            else:
                raise Exception('Variable doesnot exist')
        else:
            return(str(p))
    except:
        return 'Variable doesnot exist'

def eval_print(p):
    global env

    try:
        if p[3] == 'last':
            value = ""
            if p[1] == 'struct':
                if p[2][0] in env:
                    temp_dict = env[p[2][0]]
                    # print(f'temp_dict: {temp_dict}')
                    # print(f'p[2][1]: {p[2][1]}')
                    if p[2][1] in temp_dict:
                        temp_tuple = temp_dict[p[2][1]]
                        # print(f'temp_tuple: {temp_tuple}')
                        value = str(temp_tuple[1])
                    else:
                        raise Exception('Error')
                else:
                    raise Exception('Error')

            elif p[1] == 'str':
                value = str(p[2])

            elif p[1] == 'exp':
                value = str(eval_boolean_logic(p[2]))
                # print(value)
                if value == 'None':
                    value = "TypeError"

            elif p[1] == 'type':
                value = str(eval_exp(p[2]))

            return value
        else:
            value = ""
            if p[1] == 'struct':
                if p[2][0] in env:
                    temp_dict = env[p[2][0]]
                    if p[2][1] in temp_dict:
                        temp_tuple = temp_dict[p[2][1]]
                        # print(value)
                        value = str(temp_tuple[1])
                    else:
                        raise Exception('Error')
                else:
                    raise Exception('Error')

            elif p[1] == 'str':
                value = str(p[2])

            elif p[1] == 'exp':
                value = str(eval_boolean_logic(p[2]))
                # print(value)
                if value == 'None':
                    value = "TypeError"

            elif p[1] == 'type':
                value = str(eval_exp(p[2]))
            
            return value + " " + eval_print(p[3])   

    except:
        return 'AtributeError'
        
    

    # try:
    #     if p[2] == 'last':
    #         value = find_value_variable_in_environment(p[1])
    #         if value == 'Variable doesnot exist':
    #             raise Exception()
    #         else:
    #             return value
    #     else:
    #         value = find_value_variable_in_environment(p[1])
    #         if value == 'Variable doesnot exist':
    #             raise Exception()
    #         else:
    #             return value + " " + eval_print(p[2])       
    # except:
    #     return 'Error'


def eval_assignment(p):
    global env

    item = p[0]

    value = eval_exp(p[1][2])
    

    if item == "int":
        if type(value) == int:
            if p[1][0] == "=":
                if p[1][1] in env:
                    print("Redeclaration error")
                else:
                    env[p[1][1]] = ('int', value)
                    # print(env)
        else:
            print("Type declaration error")
    elif item == "double":
        if type(value) == float:
            if p[1][0] == "=":
                if p[1][1] in env:
                    print("Redeclaration error")
                else:
                    env[p[1][1]] = ('double', value)
                    # print(env)
        else:
            print("Type declaration error")
    elif item == "bool":
        if type(eval_boolean_logic(p[1][2])) == bool:
            if p[1][0] == "=":
                if p[1][1] in env:
                    print("Redeclaration error")
                else:
                    env[p[1][1]] = ('bool', eval_boolean_logic(p[1][2]))
                    # print(env)
        else:
            print("Type declaration error")
    elif item == "char":
        if type(value) == chr:
            if p[1][0] == "=":
                if p[1][1] in env:
                    print("Redeclaration error")
                else:
                    env[p[1][1]] = ('char', value)
                    # print(env)
        else:
            print("Type declaration error")
    elif item == "string":
        if type(eval_exp_string(p[1][2])) == str:
            if p[1][0] == "=":
                if p[1][1] in env:
                    print("Redeclaration error")
                else:
                    env[p[1][1]] = ('string', eval_exp_string(p[1][2]))
                    # print(env)
        else:
            print("Type declaration error")


def eval_exp_string(p):
    global env
    if type(p) == tuple:
        a = eval_exp_string(p[1])
        b = eval_exp_string(p[2])
        if type(a) == str and type(b) == str:
            return eval_exp_string(p[1]) + " " + eval_exp_string(p[2])
        else:
            return "Type error"
    else:
        return(p)


def eval_exp(p):
    global env

    if type(p) == tuple:
        if p[0] == "+":
            return eval_exp(p[1]) + eval_exp(p[2])
        elif p[0] == "-":
            return eval_exp(p[1]) - eval_exp(p[2])
        elif p[0] == "*":
            return eval_exp(p[1]) * eval_exp(p[2])
        elif p[0] == "/":
            if p[2] != 0:
                return eval_exp(p[1]) / eval_exp(p[2])
            else:
                return "Division by zero error"
        elif p[0] == "^":
            return pow(eval_exp(p[1]), eval_exp(p[2]))
        elif p[0] == "%":
            return eval_exp(p[1]) % eval_exp(p[2])
        elif p[0] == "var":
            if p[1] not in env:
                return "Undeclared Variable found!"
            else:
                return env[p[1]][1]

    else:
        # print(f'here{p}')
        return(p)


def eval_boolean_logic(p):
    global env

    # print(f'here: {p}')

    if type(p) == tuple:

        if p[0] == ">":
            return eval_boolean_logic(p[1]) > eval_boolean_logic(p[2])
        elif p[0] == "<":
            return eval_boolean_logic(p[1]) < eval_boolean_logic(p[2])
        elif p[0] == ">=":
            return eval_boolean_logic(p[1]) >= eval_boolean_logic(p[2])
        elif p[0] == "<=":
            return eval_boolean_logic(p[1]) <= eval_boolean_logic(p[2])
        elif p[0] == "!=":
            return eval_boolean_logic(p[1]) != eval_boolean_logic(p[2])
        elif p[0] == "==":
            return eval_boolean_logic(p[1]) == eval_boolean_logic(p[2])
        elif p[0] == "&":
            return eval_boolean_logic(p[1]) and eval_boolean_logic(p[2])
        elif p[0] == "|":
            return eval_boolean_logic(p[1]) or eval_boolean_logic(p[2])
        elif p[0] == "!":
            return not eval_boolean_logic(p[1])
        elif p[0] == "var":
            if p[1] not in env:
                return "Undeclared Variable found!"
            else:
                return env[p[1]][1]
    else:
        return eval_exp(p)



# lexer2 = Parser.lexer1
# parser2 = Parser.parser1
# while True:
#     try:
#         s = input('>> ')
#     except EOFError:
#         break
#     tree = parser2.parse(s)
#     eval_all_code(tree)


lexer2 = Parser.lexer1
parser2 = Parser.parser1
filepath = "test_cases/" + sys.argv[1]
file = open(filepath,mode='r')
all_of_it = file.read()
file.close()
tree = parser2.parse(all_of_it)
eval_all_code(tree)




