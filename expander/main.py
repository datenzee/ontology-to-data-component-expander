from pprint import pprint

from rdflib import Graph

from dc_expander import convert_rdf_class
from owl_loader import resolve_class
from util.rdf import read_rdf, write_rdf

INPUT_FILE = "input/dsco-adjusted.ttl"
ROOT_ELEMENT = "https://w3id.org/dcso/ns/core#DMP"

print(f"Expanding {INPUT_FILE} with root element {ROOT_ELEMENT}")

g = read_rdf(INPUT_FILE)
root_class = resolve_class(g, ROOT_ELEMENT)

pprint(root_class)

root_data_component = convert_rdf_class(root_class, is_root=True)

pprint(root_data_component)

output_g = Graph()
output_g.bind("dct", "http://purl.org/dc/terms/")
output_g.bind("foaf", "http://xmlns.com/foaf/0.1/")
output_g.bind("owl", "http://www.w3.org/2002/07/owl#")
output_g.bind("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
output_g.bind("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
output_g.bind("vo", "http://purl.org/datenzee/view-ontology#")
output_g.bind("xsd", "http://www.w3.org/2001/XMLSchema#")
output_g.bind("dcat", "http://www.w3.org/ns/dcat#")
output_g.bind("", "http://example.com#")

root_data_component.to_rdf(output_g)
write_rdf(output_g, "output/data_component.ttl", "turtle")

print("Finished")
