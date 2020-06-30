# Linkage Software Requirements Specification

## Output Documentation

The PDF version of the documentation is available at

[https://github.com/lbl-srg/linkage.js/blob/master/specification/build/latex/Linkage.pdf](https://github.com/lbl-srg/linkage.js/blob/master/specification/build/latex/Linkage.pdf)

The HTML version is available at

[https://lbl-srg.github.io/linkage.js](https://lbl-srg.github.io/linkage.js)

## How to Build

From `specification/.` this documentation can be built using

```
make html
```

or

```
make latex
```

It requires [Sphinx](http://www.sphinx-doc.org) and a few contributions, which can be installed by running

```
pip install sphinx sphinx_bootstrap_theme sphinxcontrib.bibtex
```

To push the subdirectory `specification/.` and rebuild GitHub Pages, run the following command from that subdirectory

```
make push
```