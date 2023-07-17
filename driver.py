import sys
from antlr4 import *
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser
from YAPLListener import YAPLListener
from graphviz import Digraph
from antlr4.tree.Trees import Trees

class MyListener(YAPLListener):
    def visitErrorNode(self, node):
        token = node.getSymbol()
        print(f"Error en la línea {token.line}: Lexema no reconocido '{token.text}'")

def visualize_tree(node, dot):
    if isinstance(node, TerminalNode):
        dot.node(str(id(node)), str(node.getSymbol().text))
    else:
        rule_name = YAPLParser.ruleNames[node.getRuleContext().getRuleIndex()]
        dot.node(str(id(node)), rule_name)
        for i in range(node.getChildCount()):
            child = node.getChild(i)
            visualize_tree(child, dot)
            dot.edge(str(id(node)), str(id(child)))

def main(argv):
    input_stream = FileStream(argv[1], encoding='utf-8')
    lexer = YAPLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = YAPLParser(stream)
    tree = parser.source()

    listener = MyListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    # Generar representación gráfica
    dot = Digraph(comment='Abstract Syntax Tree')
    visualize_tree(tree, dot)
    dot.render('tree', format='png', view=True)

    # Generar representación textual
    textual_representation = Trees.toStringTree(tree, None, parser)
    print(textual_representation)

if __name__ == '__main__':
    main(sys.argv)
