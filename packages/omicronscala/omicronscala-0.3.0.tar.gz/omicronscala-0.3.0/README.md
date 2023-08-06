# omicronscala

A python package to read .par SCALA files from Omicron.

Introduction
============
This pure Python package read .par SCALA files from Omicron.

Installation
============

```
    pip install omicronscala
```

Usage
=====

The recommended import

```
    import omicronscala
```
See the docstring help for more detailed information.

Loading
-------

To load a .par file

```
    f = omicronscala.load('path/to/file.par)
```
The instance f is a container of channels, which can be accessed by key,
and each channel has its own attributes:

```
    ch = f[0]
    ch.data
    ch.attrs
    ch.name
```

xarray dataset
--------------

The .par file can be conveniently loaded as an xarray Dataset
(provided that xarray package is installed):

```
    ds = omicronscala.to_dataset('path/to/file.par')
    ds.Z_Forward
```

NeXuS export
------------

The .par file can be converted and saved to NeXuS file with
(nxarray package is required):

```
    omicronscala.to_nexus('path/to/file.par')
```
