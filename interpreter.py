from parse import SyntaxTree
import sys

variable_env = {}

def eval_program(tree):
    if tree[1]!='empty':
        pass

    eval_block(tree[2])

def eval_block(tree):
    statement =  tree[1]
    eval_statement(statement)
    if len(tree)==3:
        eval_block(tree[2])

def eval_statement(tree):
    if tree[0]=='t_var':
        eval_declaration(tree)
    elif tree[0] == 't_initString':
        eval_initializationString(tree)
    elif tree[0] == 't_init':
        eval_initialization(tree)
    elif tree[0] == 't_assignString':
        eval_assignString(tree)
    elif tree[0] == 't_assign':
        eval_assign(tree)
    elif tree[0] == 't_print':
        eval_print(tree)
    elif tree[0] == 't_if':
        eval_if(tree)
    elif tree[0] == 't_while':
        eval_while(tree)
    elif tree[0] == 't_for':
        eval_for(tree,0)
    elif tree[0] == 't_for_range':
        eval_forRange(tree)
    elif tree[0] == 't_increment':
        eval_inc(tree)
    elif tree[0] == 't_decrement':
        eval_dec(tree)



#DECLARATION
def eval_declaration(tree):
    global variable_env
    variable_env[tree[1]] = None



#INTIALIZATION
def eval_initializationString(tree):
    global variable_env
    variable_env[tree[1]] = tree[2][1][1:-1]

def eval_initialization(tree):
    global variable_env
    if tree[2][0] == 't_or':
        val = eval_or(tree[2])
    elif tree[2][0] == 'boolean':
        val = eval_boolean(tree[2])
    variable_env[tree[1]] = val

def eval_assignString(tree):
    global variable_env
    variable_env[tree[1]] = tree[2][1][1:-1]

def eval_assign(tree):
    global variable_env
    if tree[2][0] == 't_or':
        val = eval_or(tree[2])
    elif tree[2][0] == 'boolean':
        val = eval_boolean(tree[2])
    variable_env[tree[1]] = val

#IF
def eval_if(tree):
    b = False
    if tree[1][0] == 't_or':
        b = eval_or(tree[1])
    elif tree[1][0] == 'boolean':
        b = eval_boolean(tree[1])

    if b:
        eval_block(tree[2])
    else:
        eval_elif(tree[3])

def eval_elif(tree):
    '''elif : ELSEIF  boolean  '{'  block  '}'  elif '''
    b = False
    if tree[1][0] == 't_or':
        b = eval_or(tree[1])
    elif tree[1][0] == 'boolean':
        b = eval_boolean(tree[1])

    if tree[0] == 't_elif':
        if b:
            eval_block(tree[2])
        else:
            eval_elif(tree[3])
    elif tree[0] == 't_else':
        eval_block(tree[1])
    else:
        pass

#WHILE
def eval_while(tree):
    b = False
    if tree[1][0] == 't_or':
        b = eval_or(tree[1])
    elif tree[1][0] == 'boolean':
        b = eval_boolean(tree[1])
    if b:
        eval_block(tree[2])
        eval_while(tree)
        # verify the tree passed in recursion
    else:
        pass

#FOR
def eval_for(tree,flag):
    global variable_env
    if flag==0:
        eval_initialization(tree[1])
    b = False
    if tree[2][0] == 't_or':
        b = eval_or(tree[2])
    elif tree[2][0] == 'boolean':
        b = eval_boolean(tree[2])
    if b:
        eval_block(tree[4])
        # should call unary and assign
        eval_statement(tree[3])
        eval_for(tree,1)

def eval_forRange(tree):
    global variable_env
    id = tree[1]
    val1 = eval_expression(('t_expression',tree[2]))
    val2 = eval_expression(('t_expression',tree[3]))
    for i in range(int(val1),int(val2)):
        variable_env[id] = i
        eval_block(tree[4])
        


#UNARY
def eval_inc(tree):
    global variable_env
    val = eval_id(tree[1])
    if not isinstance(val,int):
        sys.exit("Error : "+ tree[1][1]+" is not integer and cannot perform increment")
    variable_env[tree[1][1]] = val+1
def eval_dec(tree):
    global variable_env
    val = eval_id(tree[1])
    if not isinstance(val,int):
        sys.exit("Error : "+ tree[1][1]+" is not integer and cannot perform increment")
    variable_env[tree[1][1]] = val-1


#PRINT
def eval_print(tree):
    s = eval_plist(tree[1])
    print(s)
def eval_plist(tree):
    s = str(eval_pstat(tree[1]))
    if len(tree)==3:
        s+=eval_plist(tree[2])
    return s
def eval_pstat(tree):
    if tree[0]=='t_string':
        return tree[1][1:-1]
    else:
        if tree[0] == 't_or':
            val = eval_or(tree)
        elif tree[0] == 'boolean':
            val = eval_boolean(tree)
        return val


def eval_or(tree):
    global variable_env
    if tree[1][0] == 't_or':
        val1 = eval_or(tree[1])
    elif tree[1][0] == 'boolean':
        val1 = eval_boolean(tree[1])

    if tree[2][0] == 't_and':
        val2 = eval_and(tree[2])
    elif tree[2][0] == 'boolterm':
        val2 = eval_boolterm(tree[2])

    return val1 or val2


def eval_boolean(tree):
    global variable_env
    if tree[1][0] == 't_and':
        val = eval_and(tree[1])
    elif tree[1][0] == 'boolterm':
        val = eval_boolterm(tree[1])
    return val

def eval_and(tree):
    global variable_env
    if tree[1][0] == 't_and':
        val1 = eval_and(tree[1])
    elif tree[1][0] == 'boolterm':
        val1 = eval_boolterm(tree[1])

    if tree[2][0] == 't_not':
        val2 = eval_not(tree[2])
    elif tree[2][0] == 'boolterm1':
        val2 = eval_boolterm1(tree[2])
    return val1 and val2


def eval_boolterm(tree):
    global variable_env
    if tree[1][0] == 't_not':
        val = eval_not(tree[1])
    elif tree[1][0] == 'boolterm1':
        val = eval_boolterm1(tree[1])
    return val

def eval_not(tree):
    global variable_env
    if tree[1][0] == 't_condition':
        val = eval_condition(tree[1])
    elif tree[1][0] == 't_expression':
        val = eval_expression(tree[1])
    elif tree[1][0] == 't_boolvalue':
        val = eval_boolvalue(tree[1])
    return not(val)

def eval_boolterm1(tree):
    global variable_env
    if tree[1][0] == 't_condition':
        val = eval_condition(tree[1])
    elif tree[1][0] == 't_expression':
        val = eval_expression(tree[1])
    elif tree[1][0] == 't_boolvalue':
        val = eval_boolvalue(tree[1])
    return val

def eval_boolvalue(tree):
    return tree[1]

def eval_condition(tree):
    if tree[1][1][0] == 't_plus':
        val1 = eval_plus(tree[1][1])
    elif tree[1][1][0] == 't_minus':
        val1 = eval_minus(tree[1][1])
    elif tree[1][1][0] == 'expression':
        val1 = eval_expr(tree[1][1])

    if tree[1][2][0] == 't_plus':
        val2 = eval_plus(tree[1][1])
    elif tree[1][2][0] == 't_minus':
        val2 = eval_minus(tree[1][2])
    elif tree[1][2][0] == 'expression':
        val2 = eval_expr(tree[1][2])

    if tree[1][0] == 't_gt':
        return val1 > val2
    elif tree[1][0] == 't_lt':
        return val1 < val2
    elif tree[1][0] == 't_gtEql':
        return val1 >= val2
    elif tree[1][0] == 't_ltEql':
        return val1 <= val2
    elif tree[1][0] == 't_notEql':
        return val1 != val2
    elif tree[1][0] == 't_bEql':
        return val1 == val2


def eval_expression(tree):
    if tree[1][0]== 't_plus':
        val = eval_plus(tree[1])
    elif tree[1][0]== 't_minus':
        val = eval_minus(tree[1])
    elif tree[1][0]== 'expression':
        val = eval_expr(tree[1])
    return val

def eval_plus(tree):
    if tree[1][0]== 't_plus':
        val1 = eval_plus(tree[1])
    elif tree[1][0]== 't_minus':
        val1 = eval_minus(tree[1])
    elif tree[1][0]== 'expression':
        val1 = eval_expr(tree[1])

    if tree[2][0]== 't_multi':
        val2 = eval_multi(tree[2])
    elif tree[2][0]== 't_div':
        val2 = eval_div(tree[2])
    elif tree[2][0]== 'term':
        val2 = eval_term(tree[2])
    return val1+val2

def eval_minus(tree):
    if tree[1][0]== 't_plus':
        val1 = eval_plus(tree[1])
    elif tree[1][0]== 't_minus':
        val1 = eval_minus(tree[1])
    elif tree[1][0]== 'expression':
        val1 = eval_expr(tree[1])

    if tree[2][0]== 't_multi':
        val2 = eval_multi(tree[2])
    elif tree[2][0]== 't_div':
        val2 = eval_div(tree[2])
    elif tree[2][0]== 'term':
        val2 = eval_term(tree[2])
    return val1-val2

def eval_expr(tree):
    if tree[1][0]== 't_multi':
        val = eval_multi(tree[1])
    elif tree[1][0]== 't_div':
        val = eval_div(tree[1])
    elif tree[1][0]== 'term':
        val = eval_term(tree[1])
    return val

def eval_multi(tree):
    if tree[1][0]== 't_multi':
        val1 = eval_multi(tree[1])
    elif tree[1][0]== 't_div':
        val1 = eval_div(tree[1])
    elif tree[1][0]== 'term':
        val1 = eval_term(tree[1])

    if tree[2][0]== 't_id':
        val2 = eval_id(tree[2])
    elif tree[2][0]== 't_num':
        val2 = eval_num(tree[2])
    elif tree[2][0]== 't_string':
        val2 = eval_num(tree[2])
    elif tree[2][0] == 't_para':
        val2 = eval_para(tree[2])
    elif tree[2][0] == 't_ternary':
        val2 = eval_ternary(tree[2])

    return val1*val2


def eval_div(tree):
    if tree[1][0]== 't_multi':
        val1 = eval_multi(tree[1])
    elif tree[1][0]== 't_div':
        val1 = eval_div(tree[1])
    elif tree[1][0]== 'term':
        val1 = eval_term(tree[1])

    if tree[2][0]== 't_id':
        val2 = eval_id(tree[2])
    elif tree[2][0]== 't_num':
        val2 = eval_num(tree[2])
    elif tree[2][0]== 't_string':
        val2 = eval_string(tree[2])
    elif tree[2][0] == 't_para':
        val2 = eval_para(tree[2])
    elif tree[2][0] == 't_ternary':
        val2 = eval_ternary(tree[2])
    return val1/val2

def eval_term(tree):
    if tree[1][0]== 't_id':
        val = eval_id(tree[1])
    elif tree[1][0]== 't_num':
        val = eval_num(tree[1])
    elif tree[1][0]== 't_string':
        val = eval_string(tree[1])
    elif tree[1][0] == 't_para':
        val = eval_para(tree[1])
    elif tree[1][0] == 't_ternary':
        val = eval_ternary(tree[1])
    return val

def eval_id(tree):
    global variable_env
    return lookup(tree[1])
def eval_num(tree):
    return tree[1]
def eval_string(tree):
    return tree[1][1:-1]

def eval_para(tree):
    if tree[1][0]== 't_plus':
        val = eval_plus(tree[1])
    elif tree[1][0]== 't_minus':
        val = eval_minus(tree[1])
    elif tree[1][0]== 'expression':
        val = eval_expr(tree[1])
    return val

def eval_ternary(tree):
    if tree[1][0] == 't_or':
        val = eval_or(tree[1])
    elif tree[1][0] == 'boolean':
        val = eval_boolean(tree[1])
    if val:
        if tree[2][0] == 't_or':
            val1 = eval_or(tree[2])
        elif tree[2][0] == 'boolean':
            val1 = eval_boolean(tree[2])
    else:
        if tree[3][0] == 't_or':
            val1 = eval_or(tree[3])
        elif tree[3][0] == 'boolean':
            val1 = eval_boolean(tree[3])
    return val1


def lookup(x):
    global variable_env
    if x not in variable_env.keys():
        sys.exit("Error : variable "+x+" doesn't exist")
    else:
        return variable_env[x]



data = '''
var x
var y = 6
var z = "*"
var k = "&"
var x = ( y>5 ) ? (z : k)
out("The pattern by ACE:")
for(var i=0,i<5,i++){
s = ""
for(var j=0,j<5,j++){
s=s+x
}
out(s)
}
'''
builder = SyntaxTree()
builder.build(data)

print(builder.tree)
t = builder.tree
eval_program(t)
print(variable_env)
