# How to use LatticeJSON from different programming languages

This directory contains some super basic examples, which could help you to get started
working with LatticeJSON files in the programming language of your choice.

## Python

[example.py](./example.py): Python natively supports JSON files. Just import the `json` module. Alternatively you
can use `latticejson` package, which provides some convenience functions. You can
install it with:

    pip install latticejson

## Julia

[example.jl](./example.jl): Use `Pkg.add("JSON")` to install the JSON library.

## JavaScript / NodeJS

[example.js](./example.js): This example uses NodeJS. Run it with:

    node example.js


## C

[example.c](./example.c): There are several C libraries which are able to parse JSON files. For example you could
use json-c. To compile the example.c file use:

    cc example.c -ljson-c
