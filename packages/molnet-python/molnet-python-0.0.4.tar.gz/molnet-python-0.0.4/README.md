# molnet-python

A easy-to-use reimplementation of deepchem's data loading library, with minimal dependencies. With this package, you can get rid of long warnings when you use deepchem. Also, you could recognize what is going on quickly after a short time of code reviewing.

This simple library could load and split data according to [MoleculeNet](heeps://moleculenet.ai). 

This code is first written for my own, since it is tedious that you need to code the same data-loading thing every time. So, if you find this before you get to work on molecule property prediction tasks, you're lucky and please enjoy yourself!

# Installation

Currently, this package could be installed only by pip, via

```bash
pip install molnet-python
```

**NOTE**: one of dependencies, rdkit package could be installed only by `conda`, so please install rdkit before or after install this package.

# How to use

You could get splitted datasets directly from `load` function. The supported dataset names is listed in `molnet_config.py` file, except `PCBA`, all other datasets are supported. 

```python
import molnet

datasets = molnet.load(name, datadir, save_whole_dataset=False,
                       save_split=False, split=None, seed=None)
```

- `name`: dataset name
- `datadir`: where to save downloaded, extracted & cached dataset files
- `save_whole_dataset`: whether save whole dataset as a pickle binary file, useful when you have a large amount of SMILES but you need `rdkit.Chem.Mol`
- `save_split`: whether to save splitted dataset. This guarantees the consistency between different runs.
- `split`: do the corresponding data splitting
    - `(float, float, float)`: train valid test split, return 3 datasets
    - `float`: train test split, returns 2 datasets
    - `int`: K-fold cross validation split, returns K datasets
- `seed`: seed for numpy (this is useless when dataset need Scaffold split)

If you want to use lower-level functions, please review the code. I promise it won't take you more than half an hour :-)

