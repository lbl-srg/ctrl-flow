# Linkage Software Requirements Specification

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