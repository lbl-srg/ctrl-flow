# Instructions regarding the use of `sphinx`

From `specification/.` this document can be compiled  using

```
make html
```
or
```
make latex
```

The compilation requires `sphinx` (http://www.sphinx-doc.org) and a few contributions, which can be installed by running

```
pip install sphinx
pip install sphinx_bootstrap_theme
```

# Instructions regarding the use of GitHub Pages

The PDF file is available at [https://antoinegautier.github.io/linkage.js/specification/build/latex/LinkageSpec.pdf](https://antoinegautier.github.io/linkage.js/specification/build/latex/LinkageSpec.pdf).

The HTML files are hosted with GitHub Pages at [https://antoinegautier.github.io/linkage.js](https://antoinegautier.github.io/linkage.js).

To push and build the subdirectory `specification/.` run the following command from that subdirectory

```
make push
```
