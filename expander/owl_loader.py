from typing import List, Optional

from rdflib import Graph, URIRef, Literal

from util.rdf_helper import *

# RDF constants
rdf_type = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
rdfs_domain = URIRef("http://www.w3.org/2000/01/rdf-schema#domain")
rdfs_range = URIRef("http://www.w3.org/2000/01/rdf-schema#range")
rdfs_comment = URIRef("http://www.w3.org/2000/01/rdf-schema#comment")
owl_object_property = URIRef("http://www.w3.org/2002/07/owl#ObjectProperty")
owl_data_type_property = URIRef("http://www.w3.org/2002/07/owl#DatatypeProperty")


# Data classes for RDF structures
class RdfClass:
    def __init__(self, name: str, comment: Optional[str], data_types: List['RdfDataType'], objects: List['RdfObject']):
        self.name = name
        self.comment = comment
        self.data_types = data_types
        self.objects = objects

    def __repr__(self):
        return f"RdfClass(name={self.name}, comment={self.comment})"


class RdfObject:
    def __init__(self, name: str, comment: Optional[str], rdf_class: RdfClass):
        self.name = name
        self.comment = comment
        self.rdf_class = rdf_class

    def __repr__(self):
        return f"RdfObject(name={self.name}, comment={self.comment})"


class RdfDataType:
    def __init__(self, name: str, comment: Optional[str], rdf_type: str):
        self.name = name
        self.comment = comment
        self.rdf_type = rdf_type

    def __repr__(self):
        return f"RdfDataType(name={self.name}, comment={self.comment}, rdf_type={self.rdf_type})"


# Utility functions to extract URIs
def sub_uri_of(triple):
    return str(triple[0])


def obj_uri_of(triple):
    return str(triple[2])


def ob_val_of(triple):
    obj = triple[2]
    if isinstance(obj, Literal):
        return str(obj)
    return None


# Functions to resolve RDF relationships, objects, and data types
def resolve_class(graph: Graph, root_element: str) -> RdfClass:
    relationships = [sub_uri_of(triple) for triple in graph.triples((None, rdfs_domain, URIRef(root_element)))]
    return RdfClass(
        root_element,
        resolve_comment(graph, root_element),
        resolve_data_types(graph, relationships),
        resolve_objects(graph, relationships)
    )


def resolve_objects(graph: Graph, relationships: List[str]) -> List[RdfObject]:
    def is_object(r):
        type = get_object_by(graph, build_term(graph, r), rdf_type)
        return type == owl_object_property

    def create_object(o):
        return RdfObject(o, resolve_comment(graph, o), resolve_class(graph, resolve_range(graph, o)))

    return [create_object(rel) for rel in relationships if is_object(rel)]


def resolve_data_types(graph: Graph, relationships: List[str]) -> List[RdfDataType]:
    def is_data_type(r):
        type = get_object_by(graph, build_term(graph, r), rdf_type)
        return type == owl_data_type_property

    def create_data_type(d):
        return RdfDataType(d, resolve_comment(graph, d), resolve_range(graph, d))

    return [create_data_type(rel) for rel in relationships if is_data_type(rel)]


def resolve_range(graph: Graph, v: str) -> str:
    return next(obj_uri_of(triple) for triple in graph.triples((URIRef(v), rdfs_range, None)))


def resolve_comment(graph: Graph, o: str) -> Optional[str]:
    for triple in graph.triples((URIRef(o), rdfs_comment, None)):
        return ob_val_of(triple)
    return None
