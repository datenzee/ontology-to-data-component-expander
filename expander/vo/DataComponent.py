import datetime

from rdflib import Graph

from util.rdf_const import *
from util.rdf_helper import build_term


class DataComponent:
    def __init__(self, name, class_name, content):
        self.name = name
        self.class_name = class_name
        self.content = content

    def to_rdf(self, g: Graph):
        subject = build_term(g, f':{self.name}')

        g.add((subject, build_term(g, 'rdf:type'), build_term(g, "vo:DataComponent")))
        g.add((subject, build_term(g, 'rdf:type'), build_term(g, "owl:NamedIndividual")))
        g.add((subject, build_term(g, 'rdf:type'), build_term(g, "rdfs:Resource")))

        g.add((subject, build_term(g, 'vo:dataComponentName'), build_term(g, self.class_name)))

        g.add((subject, build_term(g, DC_TERMS_CREATED), build_term(g, datetime.datetime.now().isoformat())))
        g.add((subject, build_term(g, DC_TERMS_LICENSE), build_term(g, APACHE_LICENSE)))

        g.add((subject, build_term(g, 'vo:dataComponentContent'), self.content.to_rdf(g)))

        return subject
