from .filesystem import write_graph
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, SKOS, DC, OWL, XSD, RDFS
import datetime
from . import __version__
from pathlib import Path
from.config_parser import get_config_data, get_repo_name


def get_empty_prov_graph():
    bprov_uri = "http://rdf.bonsai.uno/prov/ystafdb"
    prov = Namespace("http://www.w3.org/ns/prov#")
    purl = Namespace("http://purl.org/dc/dcmitype/")
    bfoaf = Namespace("http://rdf.bonsai.uno/foaf/ystafdb#")
    bprov = Namespace("{}#".format(bprov_uri))
    dtype = Namespace("http://purl.org/dc/dcmitype/")
    vann = Namespace("http://purl.org/vocab/vann/")
    flow = "http://rdf.bonsai.uno/data/ystafdb/huse#"

    g = Graph()
    g.bind("org", "https://www.w3.org/TR/vocab-org/")
    g.bind("dtype", dtype)
    g.bind("skos", SKOS)
    g.bind("foaf", FOAF)
    g.bind("dc", DC)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("prov", prov)
    g.bind("bfoaf", bfoaf)
    g.bind("bprov", bprov)
    g.bind("vann", vann)
    g.bind("vann", vann)
    g.bind("flow", flow)

    return g


def add_prov_meta_information(g):
    bprov_uri = "http://rdf.bonsai.uno/prov/ystafdb"
    prov = Namespace("http://www.w3.org/ns/prov#")
    purl = Namespace("http://purl.org/dc/dcmitype/")
    bfoaf = Namespace("http://rdf.bonsai.uno/foaf/ystafdb#")
    bprov = Namespace("{}#".format(bprov_uri))
    dtype = Namespace("http://purl.org/dc/dcmitype/")
    vann = Namespace("http://purl.org/vocab/vann/")

    # Meta information about the Named Graph
    node = URIRef(bprov_uri)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    g.add((node, RDF.type, dtype.Dataset))
    g.add((node, DC.contributor, Literal("BONSAI team")))
    g.add((node, DC.description, Literal("Provenance information about datasets and data extraction activities")))
    g.add((node, vann.preferredNamespaceUri, URIRef(bprov)))
    g.add((node, DC.creator, bfoaf.bonsai))
    g.add((node, DC.license, URIRef("https://creativecommons.org/licenses/by/3.0/")))
    g.add((node, DC.modified, Literal(today, datatype=XSD.date)))
    g.add((node, DC.publisher, Literal("bonsai.uno")))
    g.add((node, DC.title, Literal("Provenance information")))
    g.add((node, OWL.versionInfo, Literal(__version__)))

    # Datasets in use (From config.json)
    _, datasets = get_config_data()
    for dataset in datasets:
        datasetUri = URIRef(bprov["dataset_{}".format(dataset['id'])])
        g.add((datasetUri, RDF.type, prov.Entity))
        g.add((datasetUri, DC.title, Literal(dataset['original_name'])))
        g.add(
            (
                datasetUri,
                RDFS.label,
                Literal(
                    dataset['label']
                ),
            )
        )
        g.add((datasetUri, OWL.versionInfo, Literal(dataset['version'].replace('_', '.'))))
        g.add((datasetUri, DC.term("license"), URIRef(dataset['license'])))
        g.add((datasetUri, DC.term("date"), Literal(dataset['update_date'], datatype=XSD.date)))
        g.add((datasetUri, prov.wasAttributedTo, URIRef(bfoaf["provider_{}".format(dataset['id'])])))
        g.add((datasetUri, DC.term("rights"), Literal(dataset['rights'])))
        g.add((datasetUri, prov.hadPrimarySource, URIRef(dataset['download_uri'])))

    # dataExtractionActivities
    # For each dataset, we need a new extractionActivity, this is to keep perfect lineage of data origin
    for dataset in datasets:
        arborist_uri = bprov["dataExtractionActivity_{}".format(dataset['id'])]
        g.add((arborist_uri, RDF.type, prov.Activity))
        g.add(
            (
                arborist_uri,
                RDFS.label,
                Literal(
                    "Activity to create instances of flowObjects, activityTypes "
                    "and Locations for dataset {}".format(dataset['name'])
                ),
            )
        )
        g.add((arborist_uri, prov.used, URIRef("http://ontology.bonsai.uno/core")))

        # Add usage association to
        g.add((arborist_uri, prov.used, bprov["dataset_{}".format(dataset['id'])]))

        g.add((arborist_uri, prov.hadPlan, URIRef(bprov.extractionScript)))
        g.add((arborist_uri, prov.wasAssociatedWith, URIRef(bfoaf.bonsai)))
        g.add((arborist_uri, OWL.versionInfo, Literal(__version__)))

    plan = URIRef(bprov.extractionScript)
    g.add((plan, RDF.type, prov.Plan))
    g.add((plan, RDF.type, prov.Entity))
    g.add((plan, RDFS.label, Literal("Entity representing the latest version of the YSTAFDB Script")))
    g.add((plan, prov.hadPrimarySource, URIRef("https://github.com/BONSAMURAIS/{}/tree/v{}".format(get_repo_name(), __version__.replace(".", "_")))))

    return g