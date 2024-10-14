from rdflib import Graph

from util.rdf_helper import build_term


class Tree:
    def __init__(self, name, order):
        self.name = name
        self.order = order

    def __str__(self):
        return self.name

    def to_string_full(self, indent=0):
        return '  ' * indent + '└ ' + self.name + ' (' + self.__class__.__name__ + ')\n'

    def to_rdf(self, g: Graph):
        subject = build_term(g, f':{self.name}')
        return subject
