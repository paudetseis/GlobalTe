# GlobalTe

Simple tools to extract and plot a global model of effective elastic thickness (<i>T<sub>e</sub></i>) 
of the lithosphere. This (<i>T<sub>e</sub></i>) model was obtained from the inversion of the wavelet
coherence between the topography and Bouguer gravity anomalies. See [Audet and Burgmann (2011)](#reference) 
for details.

See also the software [`PlateFlex`](https://paudetseis.github.io/PlateFlex/), which describes how to 
produce regional grids of (<i>T<sub>e</sub></i>) using the wavelet transform.

## Installation

### Dependencies

The current version was developed using **Python3.7**
Also, the following packages are required:

- [`numpy`](https://numpy.org)
- [`matplotlib`](https://matplotlib.org)
- [`cartopy`](https://scitools.org.uk/cartopy/docs/latest/#)

### Conda environment

We recommend creating a custom 
[conda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html)
where `GlobalTe` can be installed along with its dependencies. 

- Create a environment called `te` and install all dependencies:

```bash
conda create -n te python=3.7 numpy matplotlib cartopy -c conda-forge
```

- Activate the environment:

```bash
conda activate te
```

- Clone the `GlobalTe` repository and install using `pip`:

```bash
git clone https://github.com/paudetseis/GlobalTe.git
cd GlobalTe
pip install .
```


## Reference
* [Audet, P. and Burgmann, R. Dominant role of tectonic inheritance in supercontinent cycles, *Nat. Geosci.*, 4, 184-187, 2011](https://www.nature.com/articles/ngeo1080?cacheBust=1508215971286)

