from rdflib import Graph

from util.rdf_helper import build_term
from vo.Node import Node


class Container(Node):

    def to_rdf(self, g: Graph):
        subject = build_term(g, f':{self.name}')

        g.add((subject, build_term(g, 'rdf:type'), build_term(g, "vo:Container")))
        g.add((subject, build_term(g, 'rdf:type'), build_term(g, "owl:NamedIndividual")))

        g.add((subject, build_term(g, "vo:isBlock"), build_term(g, self.is_block)))
        g.add((subject, build_term(g, "vo:order"), build_term(g, self.order)))

        for child in self.contains:
            g.add((subject, build_term(g, 'vo:contains'), child.to_rdf(g)))

        return subject
