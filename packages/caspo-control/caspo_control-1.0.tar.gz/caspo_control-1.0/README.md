# caspo-control

This module brings a Python wrapper to the *control* method of the tool [caspo](https://bioasp.github.io/caspo), for the target-control of Boolean networks.

The control predictions can be processed using the [algorecell_types](https://github.com/algorecell/algorecell_types) library, which eases the
display and comparison with other control methods.

## Installation

<!--
### CoLoMoTo Notebook environment

`caspo-control` is distributed as part of the [CoLoMoTo docker](http://colomoto.org/notebook).

-->

### Using conda
```
conda install -c colomoto caspo-control
```

### Using pip

#### Extra requirements
* [clingo](https://github.com/potassco/clingo) and its Python module

```
pip install caspo_control
```

## Documentation

Documentation is available at https://caspo-control.readthedocs.io.

Examples can be found at:
* https://nbviewer.jupyter.org/github/algorecell/caspo-control/tree/master/examples/
