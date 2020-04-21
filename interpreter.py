from parse import SyntaxTree


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
    elif tree[0] == 't_print':
        eval_print(tree)




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

#IF
def eval_if(tree):
    if tree[1] == True:
        eval_block(tree)

    else:
        eval_elif(tree)

def eval_elif(tree):
    '''elif : ELSEIF  boolean  '{'  block  '}'  elif '''
    if tree[0] == 't_elif':
        if tree[1] == True:
            eval_block(tree)

        else:
            eval_elif(tree)
    else:
        eval_else(tree)

def eval_else(tree):
    if tree[0] == 't_else':
        eval_block(tree)
    else:
        pass






#PRINT
def eval_print(tree):
    s = eval_plist(tree[1])
    print(s)
def eval_plist(tree):
    s = eval_pstat(tree[1])
    if len(tree)==3:
        s+=eval_plist(tree[2])
    return s
def eval_pstat(tree):
    if tree[0]=='t_string':
        return tree[1][1:-1]
    pass


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
        val = eval_and(tree[2])
    elif tree[1][0] == 'boolterm':
        val = eval_boolterm(tree[2])
    return val

def eval_and(tree):
    global variable_env
    if tree[1][0] == 't_and':
        val1 = eval_and(tree[1])
    elif tree[1][0] == 'booleanterm':
        val1 = eval_boolterm(tree[1])

    if tree[2][0] == 't_not':
        val2 = eval_not(tree[2])
    elif tree[2][0] == 'boolterm1':
        val2 = eval_boolterm1(tree[2])

    return val1 and val2
def eval_boolterm(tree):
    global variable_env
    if tree[1][0] == 't_not':
        val = eval_not(tree[2])
    elif tree[1][0] == 'boolterm1':
        val = eval_boolterm1(tree[2])
    return val

def eval_not(tree):
    pass
def eval_boolterm1(tree):
    pass


data = '''
var z
var x = 3+4
var y = "hi"
out("hello")
'''
builder = SyntaxTree()
builder.build(data)

print(builder.tree)
t = builder.tree
eval_program(t)
print(variable_env)
