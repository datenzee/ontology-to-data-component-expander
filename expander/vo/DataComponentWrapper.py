from rdflib import Graph

from util.rdf_helper import build_term
from vo.Leaf import Leaf


class DataComponentWrapper(Leaf):
    def __init__(self, name, order, predicate, data_component):
        super().__init__(name, order)

        self.predicate = predicate
        self.data_component = data_component

    def to_rdf(self, g: Graph):
        subject = build_term(g, f':{self.name}')

        g.add((subject, build_term(g, 'rdf:type'), build_term(g, "vo:DataComponentWrapper")))
        g.add((subject, build_term(g, 'rdf:type'), build_term(g, "owl:NamedIndividual")))

        g.add((subject, build_term(g, "vo:dataComponent"), build_term(g, f':{self.data_component.name}')))
        g.add((subject, build_term(g, "vo:dataComponentPredicate"), build_term(g, self.predicate)))

        g.add((subject, build_term(g, "vo:order"), build_term(g, self.order)))

        self.data_component.to_rdf(g)

        return subject
