# qdpy - A Quality-Diversity framework for Python 3.6+

`qdpy` is a framework providing Python implementations of recent [Quality-Diversity](https://www.frontiersin.org/articles/10.3389/frobt.2016.00040/full) methodologies: [MAP-Elites](https://arxiv.org/abs/1504.04909), [CVT-MAP-Elites](https://arxiv.org/pdf/1610.05729.pdf), [NSLC](https://arxiv.org/pdf/1610.05729.pdf), [SAIL](https://arxiv.org/pdf/1702.03713.pdf), [CMA-ME](https://arxiv.org/abs/1912.02400), [ME-MAP-Elites](TBD), etc.
QD algorithms can be accessed directly, but `qdpy` also includes building blocks that can be easily assembled together to build your own QD algorithms. It can be used with parallelism mechanisms and in distributed environments.

`qdpy` includes the following features:
 * Generic support for diverse Containers: Grids, Novelty-Archives, Populations, etc
 * Optimisation algorithms for QD: random search methods, quasi-random methods, evolutionary algorithms
 * Support for multi-objective optimisation methods
 * Possible to use optimisation methods not designed for QD, such as [CMA-ES](https://arxiv.org/pdf/1604.00772.pdf)
 * Parallelisation of evaluations, using parallelism libraries, such as multiprocessing, concurrent.futures or [SCOOP](https://github.com/soravux/scoop)
 * Easy integration with the popular [DEAP](https://github.com/DEAP/deap) evolutionary computation framework


## Installation
`qdpy` requires **Python 3.6+**. It can be installed with:
```bash
pip3 install qdpy
```

`qdpy` includes optional features that need extra packages to be installed:
 * `cma` for CMA-ES support
 * `deap` to integrate with the DEAP library
 * `tables` to output results files in the HDF5 format
 * `tqdm` to display a progress bar showing optimisation progress
 * `colorama` to add colours to pretty-printed outputs

You can install `qdpy` and all of these optional dependencies with:
```bash
pip3 install qdpy[all]
```

The latest version can be installed from the GitLab repository:
```bash
pip3 install git+https://gitlab.com/leo.cazenille/qdpy.git@master
```

### To clone this repository

```bash
git clone https://gitlab.com/leo.cazenille/qdpy.git
```


## Usage

### Quickstart

The following code presents how to use MAP-Elites to explore the feature space of a target function (also available in `examples/rastrigin_short.py`):

```python
from qdpy import algorithms, containers, benchmarks, plots

# Create container and algorithm. Here we use MAP-Elites, by illuminating a Grid container by evolution.
grid = containers.Grid(shape=(64,64), max_items_per_bin=1, fitness_domain=((0., 1.),), features_domain=((0., 1.), (0., 1.)))
algo = algorithms.RandomSearchMutPolyBounded(grid, budget=60000, batch_size=500,
        dimension=3, optimisation_task="maximisation")

# Create a logger to pretty-print everything and generate output data files
logger = algorithms.AlgorithmLogger(algo)

# Define evaluation function
eval_fn = algorithms.partial(benchmarks.illumination_rastrigin_normalised,
        nb_features = len(grid.shape))

# Run illumination process !
best = algo.optimise(eval_fn)

# Print results info
print(algo.summary())

# Plot the results
plots.default_plots_grid(logger)

print("All results are available in the '%s' pickle file." % logger.final_filename)
```


`qdpy` separates Containers (here a Grid) from search algorithms, in a design inspired by [Cully2018](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7959075).
As such, to implement a MAP-Elites-style algorithm, we need to explicitly create 1) a Grid container, and 2) an evolutionary algorithm.
This algorithm will make use of this container in a similar way a classical evolutionary algorithm would use a population, and iteratively fill it with new solutions
obtained from mutation of previously explored individuals.

The target function explored in this example corresponds to the [Rastrigin function](https://en.wikipedia.org/wiki/Rastrigin_function), a classical benchmark problem for optimisation algorithms.
We translate this optimisation problem into a Quality-Diversity benchmark by defining `k` features corresponding to the first `k` parameters of the genomes of the evaluated individuals.

Here is a plot of the resulting grid of elites:
![Example of result](.description/performancesGrid.png)


### Examples
A number of examples are provided in the `examples` directory [here](https://gitlab.com/leo.cazenille/qdpy/tree/master/examples).
Here are short descriptions of all example scripts:
 * `custom_eval_fn.py`: presents how one can specify a custom evaluation function and use MAP-Elites to illuminate it.
 * `rastrigin_short.py`: the simplest example. It describes how to illuminate the rastrigin function.
 * `rastrigin.py`: a more complex version of the previous script, with support for configuration files (by default, the "conf/rastrigin.yaml" configuration file).
 * `nslc_rastrigin.py`: illumination of the rastrigin function, but with NSLC instead of MAP-Elites.
 * `artificial_landscapes.py`: illumination of several artificial landscape functions (e.g. sphere, ackley, rosenbrock, etc) by MAP-Elites. This script was used to generate the data for the GECCO 2019 poster paper [Comparing reliability of grid-based quality-diversity algorithms using artificial landscapes](https://dl.acm.org/doi/pdf/10.1145/3319619.3321895).
 * `bipedal_walker/bipedal_walker.py`: illumination of the OpenAI Gym [BipedalWalker-v2](https://gym.openai.com/envs/BipedalWalker-v2/) environment. You need to install OpenAI gym, pybullet and Box2D to use it. A more detailed README can be found [here](examples/bipedal_walker).
 * `deap_map-elites_rastrigin_short.py`, `deap_map-elites_rastrigin.py` and `deap_nslc_rastrigin.py`: three versions of the rastrigin illumination example showcasing the QDpy-DEAP integration. You need to have the DEAP library installed to use them.
 * `deap_map-elites_SR.py`: illumination of a symbolic regression problem with MAP-Elites. It relies on the QDpy-DEAP integration.

All examples generate a pickle data file containing all results and the final container/grid. It can be accessed through the following code:
```python
import pickle
# You may want to import your own packages if the pickle file contains custom objects

with open("final.p", "rb") as f:
    data = pickle.load(f)
# ``data`` is now a dictionary containing all results, including the final container, all solutions, the algorithm parameters, etc.

grid = data['container']
print(grid.best)
print(grid.best.fitness)
print(grid.best.features)
```

They also generate two PDF plots:
 * `performanceGrid.pdf`: shows the fitness score of all individual in the final grid.
 * `activityGrid.pdf`: shows the 'activity' of the algorithm. We define the activity as the number of times a cell has been updated in the grid.

More examples will be added in the future.



## Documentation
A complete documentation will be available [here](https://leo.cazenille.gitlab.io/qdpy/).


## For developers

To build `qdpy` from source:
```bash
git clone https://gitlab.com/leo.cazenille/qdpy.git
cd qdpy
./setup.py develop
```

You can run type checking (as defined in [PEP 484](https://www.python.org/dev/peps/pep-0484/) and [PEP 526](https://www.python.org/dev/peps/pep-0526/)) in the `qdpy` directory with:
```bash
mypy --ignore-missing-imports .
```

If mypy returns warnings or errors, please fix them before sending a pull request.


## Citing

```bibtex
@misc{qdpy,
    title = {QDPY: A Python framework for Quality-Diversity},
    author = {Cazenille, L.},
    year = {2018},
    publisher = {GitLab},
    journal = {GitLab repository},
    howpublished = {\url{https://gitlab.com/leo.cazenille/qdpy}},
}
```


## License

`qdpy` is distributed under the LGPLv3 license. See [LICENSE](LICENSE) for details.

