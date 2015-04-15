# GraphSim

GraphSim is a toolkit made by Bob Rubbens to simulate epidemics in graphs. It supplies functionality to generate various graphs, including Erdos-Rëny random graphs and Preferential Attachment random graphs. It can simulate infections of various shapes and sizes using arbitrary graphs and either the SIR (Susceptible, Infected, Recovered) model or the IC (Information Cascade) model. It's main purpose was facilitating a framework for doing simulations for my seventh Honours module, "Complex Networks".

It also contains (currently undocumented) functionality to generate animated movies of epidemic simulations of small graph, as demo'd here: https://www.youtube.com/watch?v=vqZQqfRWYNo

# Dependencies

- Python 3.3
- pygal (Can be installed using pip. Not needed if no charts are made)

# How to use

See simgen.py for usage examples.

# Contents

- simgen.py:        Python script that generates the data used in our report
- basicutils.py:    Helper functions of various purposes
- simutils.py:      Various functions to do SIR and IC simulations
- supergraphs.py:   The implementation of the Graph class, the foundation of this whole framework.
- graphutils.py:    Various functions for generating a variety of graphs.

# License

The MIT License (MIT)

Copyright (c) 2015 Bob Rubbens

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# Special thanks
 I want to thank Paula Felix, for teaming up with me this project, and Nelly Litvak, for her interesting lectures the second half of the module.