# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] - 2020-07-01
### Changed
- First published version is 0.5.1

## [0.5.0] - 2020-07-01
### Added
- package is published to pypi repository
### Changed
- new command line syntax:
```
usage: ystafdb-cli [-h] [-i INDIR] [-o OUTDIR] [-f {nt,ttl,xml}]

Extract rdf from ystafdb

optional arguments:
  -h, --help            show this help message and exit
  -i INDIR, --input INDIR
                        path to ystafdb csv files
  -o OUTDIR, --output OUTDIR
                        Output directory
  -f {nt,ttl,xml}, --format {nt,ttl,xml}
                        The output format

```

## [Unreleased] - 2020-06-29
### Added
- rdflib and pandas as install dependencies

