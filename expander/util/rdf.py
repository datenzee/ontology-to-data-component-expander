from rdflib import Graph


def read_rdf(file, format='turtle') -> Graph:
    g = Graph()
    g.parse(file, format=format)
    return g


def read_rdf_from_string(data, format='turtle') -> Graph:
    g = Graph()
    g.parse(data=data, format=format)
    return g


def write_rdf(content, output_file, output_format):
    f = open(output_file, "w")
    f.write(content.serialize(format=output_format).decode('utf-8'))
    f.close()
