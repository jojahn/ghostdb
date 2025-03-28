from document import GhostDocument
from parser import Parser, NodeTypes

class GhostEngine:
    def __init__(self, source: str) -> None:
        self.document = GhostDocument(source)

    def execute(self, query: str):
        parser = Parser(query)
        tree = parser.parse()
        if tree is None:
            return
        if tree.type == NodeTypes.CREATE_CMD and tree.children[0].type == NodeTypes.TABLE_SPECIFIER:
            self._create_table(tree)
        elif tree.type == 'INSERT':
            self.insert_into(tree)
        elif tree.type == 'DELETE':
            self.delete_from(tree)
        elif tree.type == 'SELECT':
            self.select_from(tree)

    def _create_table(self, tree):
        table_name = None
        columns = []
        queue = [tree]
        for node in queue:
            if node.type == NodeTypes.CREATE_CMD:
                queue.extend(node.children)
            if node.type == NodeTypes.TABLE_SPECIFIER and node.children[0].type == NodeTypes.VALUE_ARG:
                table_name = node.children[0].value
                queue.append(node.children[1])
            if node.type == NodeTypes.VALUE_LIST_ARGS:
                for child in node.children:
                    if child.type == NodeTypes.VALUE_ARG:
                        columns.append(child.value)
        if self.document.has_table(table_name):
            raise Exception("Table already exists")
        if table_name and len(columns) > 0:
            self.document.create_table(table_name, columns)

    def insert_into(self, tree):
        pass

    def delete_from(self, tree):
        pass

    def select_from(self, tree):
        pass

    def disconnect(self):
        self.document.close()

def connect(source: str) -> GhostEngine:
    return GhostEngine(source)    

