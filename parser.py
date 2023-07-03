import re, enum, math
import common


class TokenType(enum.Enum):
    WHITESPACE = 0
    NUMBER = 1
    OPERATOR = 2
    PAREN_OPEN = 3
    PAREN_CLOSE = 4
    IDENTIFIER = 5
    FUNCTION = 6
    ARG_SEPARATOR = 7
    CONSTANT = 8

class Token:
    def __init__(self, token_type, value, argument=None):
        self.type = token_type
        self.value = value

        self.argument = argument
    
    def precedence(self):
        if self.value in ("^"):
            return 2
        elif self.value in ("*", "/", "//", "%"):
            return 1
        else:
            return 0
    
    def r_associativity(self):
        if self.value in ("^"):
            return True
        else:
            return False


def str_to_tokens(inp):
    tokens = []

    curr_char = 0
    curr_token_type = None
    curr_token_val = None
    curr_function_arg = None
    while True:
        if curr_token_type in (TokenType.WHITESPACE, TokenType.PAREN_OPEN, TokenType.PAREN_CLOSE, TokenType.ARG_SEPARATOR):
            tokens.append(Token(curr_token_type, curr_token_val))
            curr_token_type = None
        
        elif curr_token_type == TokenType.NUMBER:
            if curr_char < len(inp) and curr_char < len(inp) and re.match(r"[0-9]|\.", inp[curr_char]):
                curr_token_val += inp[curr_char]
            else:
                tokens.append(Token(TokenType.NUMBER, float(curr_token_val)))
                curr_token_type = None
        
        elif curr_token_type == TokenType.OPERATOR:
            if curr_char < len(inp) and re.match(r"\/", inp[curr_char]):
                curr_token_val += inp[curr_char]
            else:
                # Check if the operator is negation and make it distinct, otherwise it will be ambiguous later on
                if curr_token_val == "-":
                    i = len(tokens) - 1
                    while True:
                        if i < 0:
                            curr_token_val = "--"
                            break
                        
                        if tokens[i].type != TokenType.WHITESPACE:
                            if tokens[i].type == TokenType.PAREN_OPEN:
                                curr_token_val = "--"
                            break

                        i -= 1
                
                if len(tokens) == 0 and curr_token_val != "--":
                    raise Exception("Expression starts with binary operator")
                if len(tokens) > 0 and tokens[-1].type == TokenType.OPERATOR:
                    raise Exception("Two consecutive operators")
                
                tokens.append(Token(TokenType.OPERATOR, curr_token_val))
                curr_token_type = None
        
        elif curr_token_type == TokenType.IDENTIFIER:
            if curr_char < len(inp) and re.match(r"[a-zA-Z0-9\$\!]", inp[curr_char]):
                curr_token_val += inp[curr_char]
            else:
                tokens.append(Token(TokenType.IDENTIFIER, curr_token_val))
                curr_token_type = None
        
        elif curr_token_type == TokenType.FUNCTION:
            if curr_char < len(inp) and re.match(r"[a-zA-Z]", inp[curr_char]):
                curr_token_val += inp[curr_char]
            elif curr_char < len(inp) and inp[curr_char] == "(":
                tokens.append(Token(TokenType.FUNCTION, curr_token_val))
                curr_token_type = None
        
        elif curr_token_type == TokenType.CONSTANT:
            if curr_char < len(inp) and re.match(r"[a-zA-Z]", inp[curr_char]):
                curr_token_val += inp[curr_char]
            else:
                tokens.append(Token(TokenType.CONSTANT, curr_token_val))
                curr_token_type = None
        
        if curr_token_type == None and curr_char < len(inp):
            if inp[curr_char].isdigit():
                curr_token_type = TokenType.NUMBER
                curr_token_val = inp[curr_char]
            elif re.match(r"\+|\-|\*|\/|\^|\%", inp[curr_char]):
                curr_token_type = TokenType.OPERATOR
                curr_token_val = inp[curr_char]
            elif inp[curr_char] == "(":
                curr_token_type = TokenType.PAREN_OPEN
                curr_token_val = inp[curr_char]
            elif inp[curr_char] == ")":
                curr_token_type = TokenType.PAREN_CLOSE
                curr_token_val = inp[curr_char]
            elif inp[curr_char] == ",":
                curr_token_type = TokenType.ARG_SEPARATOR
                curr_token_val = inp[curr_char]
            elif inp[curr_char] == "$":
                curr_token_type = TokenType.CONSTANT
                curr_token_val = ""
            elif inp[curr_char] == "!":
                curr_token_type = TokenType.IDENTIFIER
                curr_token_val = ""
            elif re.match(r"[a-zA-Z]", inp[curr_char]):
                curr_token_type = TokenType.FUNCTION
                curr_token_val = inp[curr_char]
            elif inp[curr_char] == " ":
                curr_token_type = TokenType.WHITESPACE
                curr_token_val = inp[curr_char]
            else:
                raise Exception(f"Invalid character \"{inp[curr_char]}\"")

        if curr_char == len(inp):
            break
        
        curr_char += 1

    return tokens

def tokens_to_rpn(tokens):
    # This is an implementation of the shunting yard algorithm (https://en.wikipedia.org/wiki/Shunting_yard_algorithm)
    output_queue = []
    operator_stack = []

    i = 0
    while i < len(tokens):
        if tokens[i].type == TokenType.NUMBER or tokens[i].type == TokenType.IDENTIFIER or tokens[i].type == TokenType.CONSTANT:
            output_queue.append(tokens[i])
        
        elif tokens[i].type == TokenType.FUNCTION:
            operator_stack.append(tokens[i])
        
        elif tokens[i].type == TokenType.OPERATOR:
            while len(operator_stack) != 0 and operator_stack[-1].type == TokenType.OPERATOR and \
                operator_stack[-1].precedence() >= tokens[i].precedence():

                output_queue.append(operator_stack.pop())
            operator_stack.append(tokens[i])
        
        elif tokens[i].type == TokenType.PAREN_OPEN:
            operator_stack.append(tokens[i])
        
        elif tokens[i].type == TokenType.PAREN_CLOSE:
            if len(operator_stack) == 0:
                raise Exception("Mismatched parentheses")
            
            while operator_stack[-1].type != TokenType.PAREN_OPEN:
                if len(operator_stack) == 0:
                    raise Exception("Mismatched parentheses")
                output_queue.append(operator_stack.pop())
            
            if operator_stack[-1].type != TokenType.PAREN_OPEN:
                raise Exception("Mismatched parentheses")
            operator_stack.pop()

            if len(operator_stack) > 0 and operator_stack[-1].type == TokenType.FUNCTION:
                output_queue.append(operator_stack.pop())
        
        i += 1

    while len(operator_stack) > 0:
        if operator_stack[-1].type == TokenType.PAREN_OPEN:
            raise Exception("Mismatched parentheses")
        
        output_queue.append(operator_stack.pop())
    
    return output_queue

def parse_identifier(token):
    table = None
    column = None
    row = None
    stage = 0

    for i in token.value:
        if stage == 0:
            if re.match(r"[0-9]", i):
                if table == None:
                    table = ""
                table += i
            else:
                stage = 1
        
        if stage == 1:
            if re.match(r"[A-Z]", i):
                if column == None:
                    column = ""
                column += i
            else:
                stage = 2
                if i == "$":
                    continue
        
        if stage == 2:
            if re.match(r"[0-9]", i):
                if row == None:
                    row = ""
                row += i
            else:
                raise Exception("Invalid identifier")
    
    if table == None or column == None or row == None:
        raise Exception("Invalid identifier")
    table = int(table)
    row = int(row)

    return (table, column, row)

CONSTANTS = {
    "PI": 3.1415926535897932384626433832795028841971693993751058,
    "TAU": 6.2831853071795864769252867665590057683943387987502116,
    "E": 2.71828182845904523536028747135266249775724709369995,
    "EC": 1.602176634 * 10 ** -19,
    "G": 6.67430 * 10 ** -11,
    "H": 6.62607015 * 10 ** -34,
    "C": 299792458,
    "EP": 8.8541878128 * 10 ** -12,
    "MP": 1.25663706212 * 10 ** -6,
    "ME": 9.1093837015 * 10 ** -31,
    "KB": 1.380649 * 10 ** -23,
    "NA": 6.02214076 * 10 ** 23
}
FUNCTIONS = {
    "SIN": (1, lambda x: math.sin(x[0])),
    "COS": (1, lambda x: math.cos(x[0])),
    "TAN": (1, lambda x: math.tan(x[0])),
    "ASIN": (1, lambda x: math.asin(x[0])),
    "ACOS": (1, lambda x: math.acos(x[0])),
    "ATAN": (1, lambda x: math.atan(x[0])),
    "ATAN2": (2, lambda x: math.atan2(x[0], x[1])),
    "DEG": (1, lambda x: math.degrees(x[0])),
    "RAD": (1, lambda x: math.radians(x[0])),
    "SIGN": (1, lambda x: math.copysign(1, x[0])),
    "FLOOR": (1, lambda x: math.floor(x[0])),
    "ROUND": (1, lambda x: round(x[0])),
    "CEIL": (1, lambda x: math.ceil(x[0])),
    "SQRT": (1, lambda x: math.sqrt(x[0])),
    "FACTORIAL": (1, lambda x: math.factorial(x[0])),
    "SUM": (1, lambda x: x[0]),
    "LOG": (2, lambda x: math.log(x[0], x[1])),
    "LG": (1, lambda x: math.log10(x[0])),
    "LN": (1, lambda x: math.log(x[0])),
    "ILENGTH": (1, lambda x: len(str(int(round(x[0]))))),
    "DLENGTH": (1, lambda x: len(str(x[0]).split(".")[1]))
}

def token_to_num(token):
    if token.type == TokenType.NUMBER:
        return token
    elif token.type == TokenType.IDENTIFIER:
        identifier = parse_identifier(token)
        
        if identifier[0]-1 < 0 or identifier[0]-1 >= len(common.table_data):
            raise Exception("Cell doesn't exist!")
        if common.ALPHABET.index(identifier[1]) < 0 or common.ALPHABET.index(identifier[1]) >= common.table_data[identifier[0]]["width"]:
            raise Exception("Cell doesn't exist!")
        if identifier[2] < 1 or identifier[2] > common.table_data[identifier[0]]["height"]:
            raise Exception("Cell doesn't exist!")
        
        cell_value = common.table_data[identifier[0]]["content"][common.ALPHABET.index(identifier[1])]["content"][identifier[2]]["parsed_value"]
        return Token(TokenType.NUMBER, float(cell_value))
        
    elif token.type == TokenType.CONSTANT:
        if CONSTANTS.get(token.value) == None:
            raise Exception("Unknown constant")
        else:
            return Token(TokenType.NUMBER, CONSTANTS[token.value])

def rpn_to_num(rpn):
    while len(rpn) > 1:
        for i in range(len(rpn.copy())):
            if rpn[i].type != TokenType.OPERATOR and rpn[i].type != TokenType.FUNCTION:
                continue
            
            if rpn[i].type == TokenType.OPERATOR:
                if rpn[i].value == "--":
                    arg_count = 1
                else:
                    arg_count = 2
                
                if arg_count == 2:
                    operand_1 = token_to_num(rpn[i-2])
                    operand_2 = token_to_num(rpn[i-1])
                else:
                    operand_1 = token_to_num(rpn[i-1])
                
                if rpn[i].value == "+":
                    result = operand_1.value + operand_2.value
                elif rpn[i].value == "-":
                    result = operand_1.value - operand_2.value
                elif rpn[i].value == "--":
                    result = -operand_1.value
                elif rpn[i].value == "*":
                    result = operand_1.value * operand_2.value
                elif rpn[i].value == "/":
                    result = operand_1.value / operand_2.value
                elif rpn[i].value == "^":
                    result = operand_1.value ** operand_2.value
                elif rpn[i].value == "//":
                    result = operand_1.value // operand_2.value
                elif rpn[i].value == "%":
                    result = operand_1.value % operand_2.value
                
            elif rpn[i].type == TokenType.FUNCTION:
                if FUNCTIONS.get(rpn[i].value) == None:
                    raise Exception("Unknown function")
                
                args = []
                curr_i = i
                while True:
                    curr_i -= 1
                    if curr_i < 0 or not rpn[curr_i].type in (TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.CONSTANT):
                        break
                    if len(args) == FUNCTIONS[rpn[i].value][0]:
                        break
                    args.append(token_to_num(rpn[curr_i]).value)
                
                if len(args) != FUNCTIONS[rpn[i].value][0]:
                    raise Exception("Invalid amount of arguments")
                
                arg_count = len(args)
                result = FUNCTIONS[rpn[i].value][1](args)
            
            rpn = rpn[:i-arg_count] + [Token(TokenType.NUMBER, result)] + rpn[i+1:]
            break
    
    if len(rpn) == 1:
        if not rpn[0].type in (TokenType.NUMBER, TokenType.CONSTANT, TokenType.IDENTIFIER):
            raise Exception("Invalid result")
        return token_to_num(rpn[0]).value
    else:
        return 0.0

def parse(inp):
    tokens = str_to_tokens(inp)

    rpn = tokens_to_rpn(tokens)

    ans = rpn_to_num(rpn)

    return round(ans, 15)

def increment_expression(inp):
    tokens = str_to_tokens(inp)

    incremented_tokens = []
    for t in tokens:
        if t.type == TokenType.IDENTIFIER:
            identifier = parse_identifier(t)
            if not "$" in t.value:
                incremented_identifier = Token(TokenType.IDENTIFIER, f"{identifier[0]}{identifier[1]}{identifier[2]+1}")
                incremented_tokens.append(incremented_identifier)
            else:
                incremented_tokens.append(t)
        else:
            incremented_tokens.append(t)

    result = ""
    for t in incremented_tokens:
        if t.type == TokenType.PAREN_OPEN:
            result += "("
        elif t.type == TokenType.PAREN_CLOSE:
            result += ")"
        elif t.type == TokenType.IDENTIFIER:
            result += "!"
            result += t.value
        elif t.type == TokenType.CONSTANT:
            result += "$"
            result += t.value
        else:
            result += str(t.value)
    return result

SYMBOLS = {
    "calpha": "Α",
    "alpha": "α",
    "cbeta": "Β",
    "beta": "β",
    "cgamma": "Γ",
    "gamma": "γ",
    "cdelta": "Δ",
    "delta": "δ",
    "cepsilon": "Ε",
    "epsilon": "ε",
    "epsilon2": "ϵ",
    "czeta": "Ζ",
    "zeta": "ζ",
    "ceta": "Η",
    "eta": "η",
    "ctheta": "Θ",
    "theta": "θ",
    "ciota": "Ι",
    "iota": "ι",
    "ckappa": "Κ",
    "kappa": "κ",
    "clambda": "Λ",
    "lambda": "λ",
    "cmu": "Μ",
    "mu": "μ",
    "cnu": "Ν",
    "nu": "ν",
    "cxi": "Ξ",
    "xi": "ξ",
    "comicron": "Ο",
    "omicron": "ο",
    "cpi": "Π",
    "pi": "π",
    "crho": "Ρ",
    "rho": "ρ",
    "csigma": "Σ",
    "sigma": "σ",
    "sigma2": "ς",
    "ctau": "Τ",
    "tau": "τ",
    "cupsilon": "Υ",
    "upsilon": "υ",
    "cphi": "Φ",
    "phi": "φ",
    "cchi": "Χ",
    "chi": "χ",
    "cpsi": "Ψ",
    "psi": "ψ",
    "comega": "Ω",
    "omega": "ω",
    "deg": "°",
    "u0": "⁰",
    "u1": "¹",
    "u2": "²",
    "u3": "³",
    "u4": "⁴",
    "u5": "⁵",
    "u6": "⁶",
    "u7": "⁷",
    "u8": "⁸",
    "u9": "⁹",
    "uplus": "⁺",
    "umin": "⁻",
    "ueq": "⁼",
    "ulparen": "⁽",
    "urparen": "⁾",
    "b0": "₀",
    "b1": "₁",
    "b2": "₂",
    "b3": "₃",
    "b4": "₄",
    "b5": "₅",
    "b6": "₆",
    "b7": "₇",
    "b8": "₈",
    "b9": "₉",
    "bplus": "₊",
    "bmin": "₋",
    "beq": "₌",
    "blparen": "₍",
    "brparen": "₎"
}
def parse_text(inp):
    parsed_text = ""

    current_symbol = None
    for i in inp:
        parsed_text += i
        
        if current_symbol == None and i == "&":
            current_symbol = "&"
        elif current_symbol != None:
            current_symbol += i

            if i == ";":
                sym_name = current_symbol[1:-1]
                
                if SYMBOLS.get(sym_name) != None:
                    parsed_text = parsed_text[:len(parsed_text)-len(current_symbol)] + SYMBOLS[sym_name]

                current_symbol = None
    
    return parsed_text