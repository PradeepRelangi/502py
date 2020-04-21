from parse import SyntaxTree


variable_env = {}

def eval_program(tree):
    if tree[1]!='empty':
        pass

    eval_block(tree[2])

def eval_block(tree):
    statement =  tree[1]
    print(statement[0])
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

def eval_declaration(tree):
    global variable_env
    variable_env[tree[1]] = None

def eval_initializationString(tree):
    global variable_env
    variable_env[tree[1]] = tree[2][1][1:-1]

def eval_initialization(tree):
    pass





data = '''
var z
var x = 3+4
var y = "hi"
out(x)
'''
builder = SyntaxTree()
builder.build(data)

print(builder.tree)
t = builder.tree
eval_program(t)
print(variable_env)
