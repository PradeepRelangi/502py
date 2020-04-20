import ply.yacc as yacc
import ply.lex as lex
import tokenizer

# List of token names.   This is always required
tokens = [
    'NUMBER',
    'STRING',
    'ID',
    'INCRMNT',
    'DECRMNT',
    'BOOLEQL',
    'GTEQL',
    'LTEQL',
    'NOTEQL',
    'OR',
    'AND',
    'NOT',
    'IF',
    'WHILE',
    'FOR',
    'IN',
    'RANGE',
    'VARIABLE',
    'ELSEIF',
    'ELSE',
    'PRINT',
    'FUNCTION',
    'RETURN',
    'TRUE',
    'FALSE',
]


def p_program(p):
    'program : functionlist block'
    p[0] = ('t_program', p[1],p[2])


#FUNCTION DEFINITION
def p_functionlist(p):
    '''functionlist : function functionlist
        | empty'''
    if len(p) == 3 :
        p[0] = ('t_functionlist', p[1], p[2])
    else:
        p[0] = ('empty')
def p_function(p):
    '''function : FUNCTION  ID  '('  argument  ')'  '{'  block  RETURN  boolean  '}'
            | FUNCTION ID '(' argument ')' '{' block RETURN '}' '''
    if len(p) == 11:
        p[0] = ('t_def', p[2], p[4],p[7],p[9])
    else:
        p[0] = ('t_def', p[2],p[4],p[7])
def p_argument(p):
    '''argument : ID  ','  argument
                | ID'''
    if len(p) == 3:
        p[0] = ('t_argument', p[1], p[2])
    else:
        p[0] = ('t_argument', p[1])

def p_argument_emp(p):
    '''argument : empty'''

def p_empty(p):
    ''' empty : '''
    pass


#BLOCK
def p_block(p):
    '''block : statement block
              | statement'''
    if len(p) == 3:
        p[0] = ('t_block', p[1], p[2])
    else:
        p[0] = ('t_block', p[1])

def p_statement(p):
    '''statement : declaration
                | initialization
                | assign
                | funcall
                | unary
                | while
                | for
                | if
                | print'''
    p[0] = p[1]



#DECLARATION
def p_declaration(p):
    '''declaration : VARIABLE ID'''
    p[0] = ('t_var', p[2])



#Initialization
def p_initialization_string(p):
    '''initialization : VARIABLE ID '=' STRING'''
    p[0] = ('t_assign',p[2],('t_string',p[4]))
def p_initialization(p):
    '''initialization : VARIABLE ID '=' boolean'''
    p[0] = ('t_init', p[2], p[4])



#Assign
def p_assign_string(p):
    '''assign : ID '=' STRING'''
    p[0] = ('t_assign',p[1],('t_string',p[3]))
def p_assign(p):
    '''assign : ID '=' boolean'''
    p[0] = ('t_assign', p[1], p[3])
def p_assign_funcall(p):
    '''assign : ID '=' funcall'''
    p[0] = ('t_assign', p[1], p[3])



#Unary
def p_unary(p):
    '''unary : increment
             | decrement'''
    p[0] = p[1]
def p_increment(p):
    '''increment : ID INCRMNT'''
    p[0] = ('t_increment', p[1])
def p_decrement(p):
    '''decrement : ID DECRMNT'''
    p[0] = ('t_decrmnt', p[1])




#Funcall
def p_funcall(p):
    '''funcall : ID '(' argument ')' '''
    p[0] = ('p_funcall',p[1])




#IF
def p_if(p):
    '''if : IF  boolean  '{'  block  '}'  elif '''
    p[0] = ('t_if',p[2],p[4],p[6])

def p_elif(p):
    '''elif : ELSEIF  boolean  '{'  block  '}'  elif '''
    if len(p) == 7:
        p[0] = ('t_elif',p[2],p[4],p[6])

def p_else(p):
    '''elif : ELSE  '{'  block  '}'
                | empty '''
    if len(p) == 4:
        p[0] = ('t_else',p[3])
    else:
        p[0] = ('empty')

def p_while(p):
    '''while : WHILE boolean '{' block '}' '''
    p[0] = ('t_while',p[2],p[4])




def p_for(p):
    '''for : FOR '(' initialization ';' boolean ';' assign ')' '{' block '}'
           | FOR '(' initialization ';' boolean ';' unary ')' '{' block '}'
           | FOR ID IN RANGE '(' expression ',' expression ')' '{' block '}' '''
    if len(p)== 10:
        p[0] = ('t_for',p[3],p[5],p[7],p[10])
    elif len(p)== 12:
        p[0] = ('t_for_range',p[2],p[6],p[8],p[11])



#PRINT
def p_print(p):
    '''print : PRINT '(' plist ')' '''
    p[0] = ('t_print',p[3])
def p_plist(p):
    '''plist : pstat ',' plist
             | pstat'''
    if len(p)==4:
        p[0] = (p[1],p[3])
    else:
        p[0] = p[1]
def p_pstat_str(p):
    '''pstat : STRING
             | boolean'''
    p[0] = p[1]


#Boolean
def p_boolean_or(p):
    '''boolean : boolean OR boolterm'''
    p[0] = ('t_or',p[1],p[3])
def p_boolean(p):
    '''boolean : boolterm'''
    p[0] = p[1]
def p_boolean_and(p):
    '''boolterm : boolterm AND boolterm1'''
    p[0] = ('t_and',p[1],p[3])
def p_boolterm(p):
    '''boolterm : boolterm1'''
    p[0] = p[1]
def p_boolean_not(p):
    '''boolterm1 : NOT boolterm2'''
    p[0] = ('t_not',p[2])
def p_boolterm1(p):
    '''boolterm1 : boolterm2'''
    p[0] = p[1]
def p_boolean_condition(p):
    '''boolterm2 : condition'''
    p[0] = ('t_condition',p[1])
def p_boolean_id(p):
    '''boolterm2 : expression'''
    p[0] = p[1]
def p_boolean_value(p):
    '''boolterm2 : FALSE
                 | TRUE '''
    if p[1] == 'true':
        p[0] = ('t_boolvalue',True)
    else:
        p[0] = ('t_boolvalue',False)




#condition
def p_condition_gt(p):
    '''condition : expression '<' expression'''
    p[0] = ('t_gt',p[1],p[3])
def p_condition_lt(p):
    '''condition : expression '>' expression'''
    p[0] = ('t_lt',p[1],p[3])
def p_condition_gtEql(p):
    '''condition : expression GTEQL expression'''
    p[0] = ('t_gtEql',p[1],p[3])
def p_condition_ltEql(p):
    '''condition : expression LTEQL expression'''
    p[0] = ('t_ltEql',p[1],p[3])
def p_condition_notEql(p):
    '''condition : expression NOTEQL expression'''
    p[0] = ('t_notEql',p[1],p[3])
def p_condition_bEql(p):
    '''condition : expression BOOLEQL expression'''
    p[0] = ('t_bEql',p[1],p[3])



#Expressions
def p_expression_plus(p):
    '''expression : expression '+' term'''
    p[0] = ('t_plus',p[1],p[3])

def p_expression_minus(p):
    '''expression : expression '-' term'''
    p[0] = ('t_plus',p[1],p[3])

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term_times(p):
    '''term : term '*' factor'''
    p[0] = ('t_multi',p[1],p[3])

def p_term_div(p):
    '''term : term '/' factor'''
    p[0] = ('t_div',p[1] ,p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_id(p):
 'factor : ID'
 p[0] = ('t_id',p[1])

def p_factor_num(p):
 'factor : NUMBER'
 p[0] = ('t_num',p[1])

def p_factor_expr(p):
    '''factor : '(' expression ')' '''
    p[0] = ('t_para',p[2])




# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input at:"+ str(p.value)+"  and line no:"+ str(p.lineno))




# Test it out
data = '''
    fun fact(x,y){
     z = x+y;
     send z
    }
    fun seen(z){
     z=2;
     send z
    }
    var hello=y;
    var forget;
    hello = x>y || x<y;
    if hello+3 > 5+4 || forget
    {
        var x = 3
        var y = true;
    }
    elif y==3
    {
        while z==3
        {
            x++;
            y++;
            out("hello", x+y);
        }
    }
'''
lex.lex(module=tokenizer)
# Build the parser
parser = yacc.yacc()
result = parser.parse(data)
print(result)
