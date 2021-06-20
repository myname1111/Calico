import ply.lex as lex
import ply.yacc as yacc
import sys
import copy
from decimal import *

sys.setrecursionlimit(10000)

# check if console or program:
console = False
try:
    sys.argv[1]
except IndexError:
    console = True

getcontext().prec = 32


def set_prec(p):
    getcontext().prec = int(p)
    return ""


def get_prec():
    return getcontext().prec


# Create a list to hold all of the token names
# assoc .cal calicofile
# ftype calicofile="C:\Users\Aryabima Pratama\PycharmProjects\Calico\Calico\build\exe.win-amd64-3.8\Calico.exe" "%1" %*
tokens = [

    "INT",
    "FLOAT",
    "NAME",
    "PLUS",
    "MINUS",
    "DIVIDE",
    "MULTIPLY",
    "EQUALS",
    "PAR",
    "PAL",
    "NEWLINE",
    "DSLASH",
    "COMMA",
    "COMMENT",
    "STRING",
    "DEQUALS",
    "MORE",
    "LESS",
    "MOEQ",
    "LEEQ",
    "WHILE",
    "IF",
    "ELSE",
    "ELIF",
    "TRUE",
    "FALSE",
    "LBRAC",
    "RBRAC",
    "METHOD",
    "OUTPUT"
]

# Use regular expressions to define what each token is
reserved = {
    "if": "IF",
    "elif": "ELIF",
    "else": "ELSE",
    "while": "WHILE",
    "method": "METHOD",
    "output": "OUTPUT"
}
t_DEQUALS = r"\=="
t_LESS = r"\<"
t_MORE = r">"
t_MOEQ = r"\>="
t_LEEQ = r"\<="
t_PLUS = r"\+"
t_MINUS = r"\-"
t_MULTIPLY = r"\*"
t_DIVIDE = r"\/"
t_EQUALS = r"\="
t_PAL = r"\("
t_PAR = r"\)"
t_NEWLINE = r"\;"
t_LBRAC = "\}"
t_RBRAC = "\{"
t_COMMA = r"\,"
t_COMMENT = r"\\.*\\"

t_ignore = r" "
t_ignore_tab = r" \t"


def t_FLOAT(t):
    r"\d+\.\d+"
    t.value = Decimal(t.value) * 1
    return t


def t_INT(t):
    r"\d+"
    t.value = Decimal(t.value) * 1
    return t


def t_STRING(t):
    r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
    t.type = "STRING"
    t.value = t.value.replace("\"", "")
    return t


def t_TRUE(t):
    r"true"
    t.type = "TRUE"
    t.value = True
    return t


def t_FALSE(t):
    r"false"
    t.type = "FALSE"
    t.value = False
    return t


def t_NAME(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "NAME")
    return t


def t_error(t):
    print("Illegal characters!")
    t.lexer.skip(1)


lexer = lex.lex()

precedence = (

    ("left", "NEWLINE"),
    ("none", "calc"),
    ("none", "output"),
    ("none", "while"),
    ("none", "call", "tuple"),
    ("none", "elif", "ELSE"),
    ("none", "if"),
    ("nonassoc", "LESS", "MORE", "LEEQ", "MOEQ"),
    ("left", "PLUS", "MINUS"),
    ("left", "MULTIPLY", "DIVIDE"),
    ("left", "PAR", "PAL"),
    ('right', 'UMINUS'),

)


def p_line(p):
    """
    calc : calc NEWLINE calc
    """
    p[0] = (p[2], p[1], p[3])


def p_fuc_call(p):
    """
    call : NAME tuple
    """
    p[0] = ("call", p[1], p[2])


def p_calc(p):
    """
    calc : if
         | expression
         | var_assign
         | data
         | empty
         | while
         | method
         | output
         | comment
    """
    p[0] = p[1]


def p_if_else(p):
    """
    if : IF RBRAC calc LBRAC RBRAC calc LBRAC elif
    """
    p[0] = ("if", p[3], p[6], p[8])


def p_var_assign(p):
    """
    var_assign : NAME EQUALS expression
               | NAME EQUALS data
    """
    p[0] = ("=", p[1], p[3])


def elif_floor(p):
    """
    elif : ELSE RBRAC calc LBRAC
    """
    p[0] = ("else", p[3])


def p_if(p):
    """
    if : IF RBRAC calc LBRAC RBRAC calc LBRAC
    """
    p[0] = ("if", p[3], p[6])


def p_expression_uminus(p):
    """expression : MINUS expression %prec UMINUS"""
    p[0] = -p[2]


def p_expression(p):
    """
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
               | expression MORE expression
               | expression LESS expression
               | expression MOEQ expression
               | expression LEEQ expression
               | expression DEQUALS expression
    """
    p[0] = (p[2], p[1], p[3])


def p_expression_floor(p):
    """
    expression : INT
               | FLOAT
               | call
               | TRUE
               | FALSE
    """
    p[0] = p[1]


def p_expression_par(p):
    """
    expression : PAL expression PAR
    """
    p[0] = p[2]


def p_expression_var(p):
    """
    expression : NAME
    """
    p[0] = ("var", p[1])


def p_comma(p):
    """
    data : data COMMA data
    """
    p[0] = (p[2], p[1], p[3])


def p_data_floor(p):
    """
    data : string
         | INT
         | FLOAT
         | tuple
         | expression
         | empty
    """
    p[0] = p[1]


def p_string(p):
    """
    string : STRING
    """
    p[0] = ("string", p[1])


def p_tuple(p):
    """
    tuple : PAL data PAR
    """
    p[0] = ("tuple", p[2])


def p_while(p):
    """
    while : WHILE RBRAC expression LBRAC RBRAC calc LBRAC
    """
    p[0] = ("while", p[3], p[6])


def p_return(p):
    """
    output : OUTPUT expression
    """
    p[0] = ("output", p[2])


def p_def(p):
    """
    method : METHOD NAME tuple RBRAC calc LBRAC
    """
    p[0] = ("method", p[2], p[3], p[5])


def p_elif(p):
    """
    elif : ELIF RBRAC calc LBRAC RBRAC calc LBRAC
    """
    p[0] = ("elif", p[3], p[6])


def p_elif_else(p):
    """
    elif : ELIF RBRAC calc LBRAC RBRAC calc LBRAC elif
    """
    p[0] = ("elif", p[3], p[6], p[9])


def p_empty_com(p):
    """
    empty : none
          | comment
    """
    p[0] = p[1]


def p_empty(p):
    """
    none :
    """
    p[0] = None


def p_comment(p):
    """
    comment : COMMENT
    """
    p[0] = None


def p_error(p):
    print(f"Error detected:{p}")


lex.lex(errorlog=lex.NullLogger())
yacc.yacc(errorlog=yacc.NullLogger())
is_compiler = True
parser = yacc.yacc()

env = {
    "variables": {
        "float_prec": getcontext().prec
    },
    "functions": {},
    "builtins": {
        "print": print,
        "input": input,
        "int": Decimal,
        "get_prec": get_prec,
        "set_prec": set_prec,
    }
}

out = ""


def run(p, local_env=None):
    global env, a
    if local_env is None:
        local_env = env
    global is_compiler
    if type(p) == tuple:
        if p[0] == "+":
            return run(p[1], local_env) + run(p[2], local_env)
        elif p[0] == "-":
            return run(p[1], local_env) - run(p[2], local_env)
        elif p[0] == "*":
            return run(p[1], local_env) * run(p[2], local_env)
        elif p[0] == "/":
            return run(p[1], local_env) / run(p[2], local_env)
        elif p[0] == ">":
            return run(p[1], local_env) > run(p[2], local_env)
        elif p[0] == "<":
            return run(p[1], local_env) < run(p[2], local_env)
        elif p[0] == "==":
            return run(p[1], local_env) == run(p[2], local_env)
        elif p[0] == ">=":
            return run(p[1], local_env) >= run(p[2], local_env)
        elif p[0] == "<=":
            return run(p[1], local_env) <= run(p[2], local_env)
        elif p[0] == "var":
            try:
                return run(local_env["variables"][p[1]])
            except KeyError:
                return p[1]
        elif p[0] == "=":
            local_env["variables"][p[1]] = run(p[2], local_env)
            return ""
        elif p[0] == ";":
            run(p[1], local_env)
            run(p[2], local_env)
            return ""
        elif p[0] == "comment":
            return ""
        elif p[0] == "string":
            return str((p[1]))
        elif p[0] == "tuple":
            r = run(p[1], local_env)
            try:
                if type(r) != tuple and type(r) != list:
                    return r
                else:
                    a = tuple(r)
            except TypeError:
                a = r
            return a
        elif p[0] == ",":
            a = [run(p[1], local_env)]
            b = [run(p[2], local_env)]
            try:
                b = a + b
            except TypeError:
                b = [p[1]] + [p[2]]
            return b
        elif p[0] == "call":
            if p[1] in local_env["builtins"]:
                a = local_env["builtins"][p[1]]
                a = a(run(p[2], local_env))
                return a
            elif p[1] in local_env["functions"]:
                temp1 = local_env["functions"][p[1]]
                local = copy.deepcopy(temp1)
                func_env = local["env"]
                var = local["param"]
                in_param = run(p[2], local_env)
                dict_param_var = {}
                lent = 0
                try:
                    for i in var:
                        dict_param_var[i] = in_param[lent]
                        lent += 1
                except TypeError:
                    for i in var:
                        dict_param_var[i] = in_param
                        lent += 1
                func_env["variables"].update(dict_param_var)
                run(local["code"], func_env)
                return func_env["output"]
        elif p[0] == "if" or p[0] == "elif":
            if run(p[1], local_env):
                run(p[2], local_env)
            else:
                try:
                    run(p[3], local_env)
                except IndexError:
                    pass
            return ""
        elif p[0] == "while":
            while run(p[1], local_env):
                run(p[2], local_env)
            return ""
        elif p[0] == "method":
            param = []
            if type(run(p[2])) == tuple:
                for z in run(p[2], local_env):
                    param.append(z)
            else:
                param.append(run(p[2]))
            local_env["functions"][p[1]] = {
                "param": tuple(param),
                "code": p[3],
                "env": {
                    "variables": {},
                    "builtins": {
                        "print": print,
                        "input": input,
                        "int": int
                    },
                    "functions": local_env["functions"]
                },
            }
        elif p[0] == "output":
            local_env["output"] = run(p[1], local_env)
            return ""

    elif type(p) == Decimal:
        return p * 1
    else:
        return p


while console:
    try:
        try:
            s = input("in: ")
        except EOFError:
            break
        print(s)
        s = parser.parse(s)
        run(s)
    except Exception as e:
        print(f"there was an error while running: {e}")
if not console:
    try:
        dir_cal = sys.argv[1]
        with open(dir_cal, "r") as a:
            s = a.read()
        s = s.replace("\n", "")
        s = parser.parse(s)
        run(s)
    except Exception as e:
        print(f"there was an error while running: {e}")
        input("press any key to exit")
