__package__ = "transformer"
from lark import Lark, Transformer
import grammar

class IPOTransformer(Transformer):
    def compare(self, items):
        return {'type': 'compare','left': items[0], 'op': items[1],'right': items[2]
        }
    
    def assignment(self, items):
        return {'type': 'assignment', 'variable': items[0], 'value': items[1]}

    def start(self, items):
        return items[0]

    def if_stmt(self, items):
        condition = items[0]
        then_block = items[1]
        else_block = items[2] if len(items) > 2 else None
        return {'type': 'if', 'condition': condition, 'then': then_block, 'else': else_block}

    def condition(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {'type': 'logic', 'op': items[1], 'left': items[0], 'right': items[2]}
        else:
            return items[1]  # Parentheses case

    def compare_expr(self, items):
        return {'type': 'compare', 'left': items[0], 'op': items[1], 'right': items[2]}

    # def logic_op(self, item):
    #     return item[0]
    
    # def compare_op(self, item):
    #     return item[0]
    
    def IDENTIFIER(self, token):
        return {'type': 'identifier', 'name': token.value}
    
    def NUMBER(self, token):
        try:
            # Attempt to convert to integer first
            return {'type': 'number', 'value': int(token.value)}
        except ValueError:
            return {'type': 'number', 'value': float(token.value)}    
    
    def value(self, item):
        return item[0]
    
    def then_block(self, items):
        return {'type': 'block', 'statements': items}
    
    def else_block(self, items):
        return {'type': 'block', 'statements': items}
    
    def arithmetic_stmt(self, items):
        return {'type': 'arithmetic', 'variable': items[0], 'expression': items[1]}
    def evaluation_stmt(self, items):
        conditions = []
        for i in range(1, len(items) - 1, 2):
            conditions.append({'type': 'condition', 'id': items[i], 'statements': items[i + 1]})
        return {'type': 'evaluation', 'id': items[0], 'conditions': conditions}
    def call_stmt(self, items):
        return {'type': 'call', 'function': items[0]}
    def repeat_until_stmt(self, items):
        return {'type': 'repeat_until','condition': items[0],'block': items[1:]}
    def arithmetic_expr(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {'type': 'arithmetic', 'left': items[0], 'op': items[1], 'right': items[2]}
        else:
            return {'type': 'arithmetic', 'expression': items[0]}
    def logic_op(self, items):
        return {'type': 'logic_op', 'value': items[0]}
    def compare_op(self, items):
        return {'type': 'compare_op', 'value': items[0]}
    def arithmetic_op(self, items):
        return {'type': 'arithmetic_op', 'value': items[0]}
