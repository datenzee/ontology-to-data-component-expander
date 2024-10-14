from rdflib import Graph

from util.rdf_helper import build_term
from vo.Leaf import Leaf


class Content(Leaf):
    def __init__(self, name, order, predicate=None, contentContent=None, content=None):
        super().__init__(name, order)
        self.predicate = predicate
        self.contentContent = contentContent
        self.content = content

    def to_rdf(self, g: Graph):
        subject = build_term(g, f':{self.name}')

        type = 'vo:Content'
        if self.content == 'Email':
            type = 'vo:Email'
        elif self.content == 'DateTime':
            type = 'vo:DateTime'
        elif self.content == 'Date':
            type = 'vo:Date'
        elif self.content == 'Url':
            type = 'vo:URL'

        g.add((subject, build_term(g, 'rdf:type'), build_term(g, type)))
        g.add((subject, build_term(g, 'rdf:type'), build_term(g, "owl:NamedIndividual")))

        g.add((subject, build_term(g, 'vo:order'), build_term(g, self.order)))

        if self.predicate is not None:
            g.add((subject, build_term(g, 'vo:contentPredicate'), build_term(g, self.predicate)))
        if self.contentContent is not None:
            g.add((subject, build_term(g, 'vo:contentContent'), self.contentContent.to_rdf(g)))

        return subject
