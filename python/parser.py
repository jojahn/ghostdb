from enum import Enum

"""
COMMAND [SPECIFIER] ARGS SPECIFIER_ARGS
Examples:
    CREATE TABLE table_name (column_name,column_name)
    INSERT INTO table_name VALUES (value,value)
    SELECT * FROM table_name
"""

class TokenTypes(Enum):
    VALUE = 0
    VALUE_LIST_START = 1
    VALUE_LIST_END = 2

class TokenNode:
    def __init__(self, type: TokenTypes, value: str):
        self.type = type
        self.value = value

    def  __repr__(self):
        return f"Tok({self.type.name}, '{self.value}')"

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.tokens = []

    def tokenize(self):
        token_buffer = []
        token_handled = False
        for token in list(self.text):
            if token == ' ':
                token_handled = True
            if token == '(':
                self.tokens.append(TokenNode(type=TokenTypes.VALUE_LIST_START, value=token))
                token_handled = True
            elif token == ')':
                self.tokens.append(TokenNode(type=TokenTypes.VALUE_LIST_END, value=token))
            elif token == ',':
                token_handled = True

            if token_handled and len(token_buffer) > 0:
                if token_buffer == "CREATE":
                    self.tokens.append(TokenNode(type=TokenTypes.VALUE, value="CREATE"))
                elif token_buffer == "TABLE":
                    self.tokens.append(TokenNode(type=TokenTypes.VALUE, value="TABLE"))
                else:
                    self.tokens.append(TokenNode(type=TokenTypes.VALUE, value="".join(token_buffer)))
                token_buffer = []
            elif not token_handled:
                token_buffer.append(token)
            else:
                token_buffer = []
            token_handled = False
        return self.tokens
            

class NodeTypes(Enum):
    CREATE_CMD = "CREATE"
    INSERT_CMD = "INSERT"
    SELECT_CMD = "SELECT"
    WHERE_SPECIFIER = "WHERE"
    VALUES_SPECIFIER = "VALUES"
    CONDITION_ARGS = "CONDITION"
    VALUE_LIST_ARGS = "VALUE_LIST"
    VALUE_ARG = "VALUE"
    TABLE_SPECIFIER = "TABLE"

class ParserNode:
    def __init__(self, parent, type: NodeTypes, value: str):
        self.type = type
        self.value = value
        self.children = []
        self.parent = parent

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        parent_str = self.parent.type.name if self.parent is not None else "None"
        result = f"AST({self.type.name}, '{self.value}') < {parent_str}\n"
        for child in self.children:
            if child is not None:
                result += f"  {child}\n"
        return result

class Parser:
    def __init__(self, text: str):
        self.lexer = Lexer(text)
        self.tokens = []
    """
    CREATE
      TABLE
        table_name  VALUES
                      (column_name,column_name)
    """
    def parse(self):
        self.tokens = self.lexer.tokenize()
        tree = None
        parent = None
        last_node = None
        for token in self.tokens:
            if tree is None:
                if token.value == 'CREATE':
                    last_node = ParserNode(None, NodeTypes.CREATE_CMD, 'CREATE')
                    tree = last_node
                    parent = last_node
                elif token.value == "INSERT":
                    last_node = ParserNode(None, NodeTypes.INSERT_CMD, 'INSERT')
                    tree = last_node
                    parent = last_node
                elif token.value == 'SELECT':
                    last_node = ParserNode(None, NodeTypes.SELECT_CMD, 'SELECT')
                    tree = last_node
                    parent = last_node
                else:
                    raise Exception("Invalid token", token)
            else:
                if last_node.type == NodeTypes.CREATE_CMD:
                    if token.value == NodeTypes.TABLE_SPECIFIER.value:
                        child = ParserNode(parent, NodeTypes.TABLE_SPECIFIER, token.value)
                        parent.add_child(child)
                        last_node = child
                        parent = child
                    else:
                        raise Exception("Invalid token", token, last_node)
                elif last_node.type == NodeTypes.TABLE_SPECIFIER:
                    if token.type == TokenTypes.VALUE:
                        child = ParserNode(parent, NodeTypes.VALUE_ARG, token.value)
                        parent.add_child(child)
                        last_node = child
                    else:
                        raise Exception("Invalid token", token, last_node)
                    
                elif last_node.type == NodeTypes.VALUE_ARG and parent.type == NodeTypes.TABLE_SPECIFIER:
                    if token.type == TokenTypes.VALUE_LIST_START:
                        child = ParserNode(parent, NodeTypes.VALUE_LIST_ARGS, token.value)
                        parent.add_child(child)
                        last_node = child
                        parent = child
                    else:
                        raise Exception("Invalid token", token, last_node)
                elif last_node.type == NodeTypes.VALUE_LIST_ARGS:
                    if token.type == TokenTypes.VALUE:
                        parent.add_child(ParserNode(parent, NodeTypes.VALUE_ARG, token.value))
                    elif token.type == TokenTypes.VALUE_LIST_END:
                        last_node = tree
                        parent = parent.parent
                    else:
                        raise Exception("Invalid token", token, last_node)
        return tree
            
        

if __name__ == '__main__':
    parser = Parser("CREATE TABLE table_name (column_name,column_name)")
    tree = parser.parse()
    print("tokens", parser.tokens)
    print(f"tree: \n{tree}")
