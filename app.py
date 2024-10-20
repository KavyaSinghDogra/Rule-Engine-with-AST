from flask import Flask, render_template, request, jsonify
from node import Node, parse_rule_string, combine_rule_strings, evaluate_ast

app = Flask(__name__)

# In-memory store for rules (in real-world, you would use a database)
rules = {}

# Route to serve the HTML page (UI)
@app.route('/')
def index():
    return render_template('index.html')

# API to create a rule from a rule string and store its AST representation
@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json.get('rule')
    ast = parse_rule_string(rule_string)
    rules[rule_string] = ast  # Store the AST in memory
    return jsonify({"message": "Rule created", "rule": rule_string})

# API to combine multiple rules into a single AST
@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    rule_strings = request.json.get('rules')
    combined_ast = combine_rule_strings(rule_strings, rules)
    return jsonify({"combined_ast": repr(combined_ast)})

# API to evaluate a rule AST against input data
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    rule_string = request.json.get('rule')
    data = request.json.get('data')
    ast = rules.get(rule_string)
    if ast:
        result = evaluate_ast(ast, data)
        return jsonify({"result": result})
    return jsonify({"error": "Rule not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
