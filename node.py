import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left       # left child node
        self.right = right     # right child node
        self.value = value     # value for operand nodes (e.g., number, string)
        
    def __repr__(self):
        return f"Node(type={self.type}, value={self.value})"

# Parse rule string into tokens and build AST
def parse_rule_string(rule_string):
    tokens = tokenize(rule_string)
    return build_ast(tokens)

# Tokenize the rule string
def tokenize(rule_string):
    return re.findall(r'\w+|\(|\)|>|<|=|AND|OR', rule_string)

# Build AST from tokens
def build_ast(tokens):
    if not tokens:
        return None
    
    token = tokens.pop(0)
    if token == '(':
        left = build_ast(tokens)
        operator = tokens.pop(0)
        right = build_ast(tokens)
        tokens.pop(0)  # Pop ')'
        return Node('operator', left, right, operator)
    else:
        return Node('operand', value=token)

# Combine multiple rules into a single AST using AND
def combine_rule_strings(rule_strings, rules):
    combined_ast = None
    for rule_string in rule_strings:
        ast = rules.get(rule_string)
        if combined_ast is None:
            combined_ast = ast
        else:
            combined_ast = Node('operator', left=combined_ast, right=ast, value='AND')
    return combined_ast

# Evaluate the AST against data
def evaluate_ast(node, data):
    if node.type == 'operand':
        key, operator, value = node.value.split()
        if operator == '>':
            return data.get(key) > int(value)
        elif operator == '<':
            return data.get(key) < int(value)
        elif operator == '=':
            return data.get(key) == value
    elif node.type == 'operator':
        if node.value == 'AND':
            return evaluate_ast(node.left, data) and evaluate_ast(node.right, data)
        elif node.value == 'OR':
            return evaluate_ast(node.left, data) or evaluate_ast(node.right, data)
    return False
