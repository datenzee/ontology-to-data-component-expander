from rdflib import Graph, Literal

from util.rdf_helper import build_term
from vo.Leaf import Leaf


class TextContent(Leaf):
    def __init__(self, name, order, value=None):
        super().__init__(name, order)
        self.value = value

    def to_rdf(self, g: Graph):
        subject = build_term(g, f':{self.name}')

        g.add((subject, build_term(g, 'rdf:type'), build_term(g, "vo:TextContent")))
        g.add((subject, build_term(g, 'rdf:type'), build_term(g, "owl:NamedIndividual")))

        g.add((subject, build_term(g, 'vo:textContentValue'), Literal(self.value)))

        return subject
