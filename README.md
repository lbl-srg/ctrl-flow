# LinkageJS Requirements Specification

## Output Documentation

The PDF version of the documentation is available at

[https://github.com/AntoineGautier/linkage.js/blob/master/specification/build/latex/LinkageJS.pdf](https://github.com/AntoineGautier/linkage.js/blob/master/specification/build/latex/LinkageJS.pdf)

The HTML version is available at

[https://antoinegautier.github.io/linkage.js](https://antoinegautier.github.io/linkage.js)

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
pip install sphinx
pip install sphinx_bootstrap_theme
```

To push the subdirectory `specification/.` and rebuild GitHub Pages, run the following command from that subdirectory

```
make push
```