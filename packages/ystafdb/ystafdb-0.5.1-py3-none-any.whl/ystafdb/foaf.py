from .filesystem import write_graph
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, SKOS, DC, OWL, XSD
import datetime
from . import __version__
from .config_parser import get_config_data


def generate_foaf_uris(args):
    """Note the URIs needed for units. They all come from the Ontology of Units
    of Measure."""
    output_base_dir = Path(args.outdir)

    org = Namespace("https://www.w3.org/TR/vocab-org/")
    prov = Namespace("http://www.w3.org/ns/prov#")
    purl = Namespace("http://purl.org/dc/dcmitype/")
    bfoaf = Namespace("http://rdf.bonsai.uno/foaf/ystafdb#")
    dtype = Namespace("http://purl.org/dc/dcmitype/")
    vann = Namespace("http://purl.org/vocab/vann/")

    g = Graph()
    g.bind("vann", vann)
    g.bind("org", org)
    g.bind("dtype", dtype)
    g.bind("skos", SKOS)
    g.bind("foaf", FOAF)
    g.bind("dc", DC)
    g.bind("owl", OWL)
    g.bind("prov", prov)
    g.bind("bfoaf", bfoaf)

    node = URIRef("http://rdf.bonsai.uno/foaf/ystafdb")

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    g.add((node, RDF.type, dtype.Dataset))
    g.add((node, DC.creator, bfoaf.bonsai))
    g.add((node, DC.contributor, Literal("BONSAI team")))
    g.add((node, DC.description, Literal("Instances of Organizations")))
    g.add((node, vann.preferredNamespaceUri, URIRef(bfoaf)))
    g.add((node, DC.license, URIRef("https://creativecommons.org/licenses/by/3.0/")))
    g.add((node, DC.modified, Literal(today, datatype=XSD.date)))
    g.add((node, DC.publisher, Literal("bonsai.uno")))
    g.add((node, DC.title, Literal("Organizations")))
    g.add((node, OWL.versionInfo, Literal(__version__)))

    node = URIRef(bfoaf.bonsai)
    g.add((node, RDF.type, org.Organization))
    g.add((node, RDF.type, prov.Agent))
    g.add(
        (
            node,
            SKOS.prefLabel,
            Literal(
                "BONSAI – Big Open Network for Sustainability Assessment Information"
            ),
        )
    )
    g.add((node, FOAF.homepage, URIRef("https://bonsai.uno")))
    g.add((node, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q131201")))
    g.add((node, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q2323664")))
    g.add((node, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q18692990")))

    # Dataset providers, comes from config.json file
    providers, _ = get_config_data()
    for provider in providers:
        providerUri = URIRef(bfoaf["provider_{}".format(provider['id'])])
        g.add((providerUri, RDF.type, org.Organization))
        g.add((providerUri, RDF.type, prov.Agent))
        g.add((providerUri, DC.title, Literal(provider['name'])))
        g.add(
            (
                providerUri,
                DC.description,
                Literal(provider['label'])
            )
        )
        g.add((providerUri, FOAF.homepage, URIRef(provider['homepage'])))

    write_graph(output_base_dir / "foaf" / "ystafdb", g, args.format)
