# Linkage Software Requirements Specification

Linkage is a graphical user interface for configuring models of HVAC and control systems for use
with the Modelica Buildings Library (https://simulationresearch.lbl.gov/modelica/)
and for use of the ASHRAE Standard 231P that is currently in development.
Support for control specification will be via an export of the control sequence in the Control Description Language
of the OpenBuildingControl project (https://obc.lbl.gov) that is now under further development in ASHRAE 231P,
and an export of documents for bidding and implementation of building control sequences.

The model content of linkage is driven by a json representation that is generated from
the Modelica Buildings Library using https://github.com/lbl-srg/modelica-json.

This repository documents the requirements and design of Linkage.

## Output Documentation


The HTML version of the documentation is available at
[lbl-srg.github.io/linkage.js](https://lbl-srg.github.io/linkage.js)

The PDF version of the documentation is available at
[github.com/lbl-srg/linkage.js/blob/master/specification/build/latex/Linkage.pdf](https://github.com/lbl-srg/linkage.js/blob/master/specification/build/latex/Linkage.pdf)

## How to Build

From `specification/.` this documentation can be built using

```
make html
```

or

```
make latex
```

It requires [Sphinx](http://www.sphinx-doc.org) (>=3.1) and a few contributions, which can be installed by running

```
pip install sphinx sphinx_bootstrap_theme sphinxcontrib.bibtex
```

To push the subdirectory `specification/.` and rebuild GitHub Pages, run the following command from that subdirectory

```
make push
```
