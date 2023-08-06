# YSTAFDB

YSTAFDB creates turtle files of the istances of data based on an ontology.
The turtle files are needed for the BONSAI knowledge graph.

The turtle files generated are stored in the BONSAI [rdf repository](https://github.com/BONSAMURAIS/rdf).

Currently generates the following:

* Activity types, flow objects, locations and flows for YSTAFDB v1.0.

## Installation

### with package manager pip from pypi

Installable via `pip`:

```
pip install ystafdb
```

### manual

Clone git repo
```
$ git clone git@github.com:BONSAMURAIS/ystafdb.git
```

Enter cloned repo
```
$ cd ystafdb
```

Now install package

```
$ python setup.py install
```

## Usage

You must first download the Base Data, and then use `ystafdb-cli` to produce the ttl/nt/xml files.

### Download Base Data

The data can be downloaded [here](https://www.sciencebase.gov/catalog/file/get/5b9a7c28e4b0d966b485d915?f=__disk__0f%2F58%2Fa7%2F0f58a74db669ee5418f36a698bc85781e867e0ab) as a zip file.

Extract the contents of the zip file. As an example, the data can be placed under `ystafdb-input`.
The following files from the Base Data are _mandatory_ to have in the folder (`ystafdb-input` in our example):

- `material_names.csv`
- `subsystems.csv`
- `flows.csv`
- `publications.csv`
- `reference_spaces.csv`
- `reference_materials.csv`
- `reference_timeframes.csv`


Under a Linux terminal, you can acomplish the previous two operations with:

```
curl -L "https://www.sciencebase.gov/catalog/file/get/5b9a7c28e4b0d966b485d915?f=__disk__0f%2F58%2Fa7%2F0f58a74db669ee5418f36a698bc85781e867e0ab" -o YSTAFDB_CSV_files.zip
unzip -d ystafdb-input YSTAFDB_CSV_files.zip
```

### Generate the ttl or nt or xml files

If the package is correctly installed, you can use the command line tool `ystafdb-cli` to produce the rdfs as follows:

```
$ ystafdb-cli -i <inputdir> -o <outputdir>
```


Where:
+ `<inputdir>` is the location of the ystafdb csv files, and 
+ `<outputdir>` is the directory where the output triples graphs will be placed. This is optional,
  if not supplied, the output directory will be `output`

In the Linux terminal example from above, this would be done with:

```
ystafdb-cli -i ystafdb-input
```

The `<outputdir>` directory will have the following contents:

```
output
├── [ 4.0K]  activitytype
│   └── [ 4.0K]  ystafdb
│       └── [ 249K]  ystafdb.ttl
├── [ 4.0K]  flow
│   └── [ 4.0K]  ystafdb
│       └── [ 4.0K]  huse
│           └── [  41M]  huse.ttl
├── [ 4.0K]  flowobject
│   └── [ 4.0K]  ystafdb
│       └── [  63K]  ystafdb.ttl
├── [ 4.0K]  foaf
│   └── [ 4.0K]  ystafdb
│       └── [ 1.4K]  ystafdb.ttl
├── [ 4.0K]  location
│   └── [ 4.0K]  ystafdb
│       └── [ 158K]  ystafdb.ttl
└── [ 4.0K]  prov
    └── [ 4.0K]  ystafdb
        └── [ 1.0M]  ystafdb.ttl
```

## Contributing
All contributions should be via pull request, do not edit this package directly! We actually use it for stuff.

