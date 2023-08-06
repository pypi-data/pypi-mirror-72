# pso_solver
A package that implements the particle swarm optimization algorithm.
Particle swarm optimization (PSO) is a computational technique used to find the global optimum of a function,
introduced in 1995 by Kennedy and Eberhardt.
Candidate solutions for the optimum of the function, called particles, are initialized in the search space randomly,
and move through several iterations towards the global optimimum guided by
* The locally best known position of the particle (pBest)
* The globally best known position among all the particles (gBest)

'Best' position refers to the location in space that tends to minimize/maximize the function.
The relative importance of the influence of pBest and gBest on the motion of a particle is determined by parameters c1 and c2, respectively.
The speed of the particle is defined by v, and its contribution is determined by the weight factor W.
Make sure v and W are neither too large nor too small.
Too large a value of v or W cause some particles to overshoot and move towards infinity.
Using too small a value will however slow down convergence.
Selecting the best parameters c1, c2 and W is experimental, and has to be done through trial and error.

Reference:
Eberhart, R., & Kennedy, J. (1995, November). Particle swarm optimization. In Proceedings of the IEEE international conference on neural networks (Vol. 4, pp. 1942-1948). Citeseer.

# Examples

## Cosine function
10 particles, 50 iterations, c1=1, c2=1, W=0.5

<img src="https://github.com/nikhilkmr300/pso_solver/blob/master/images/cosine.png" width="320" height="240">

Particles approaching the minimum of the cosine function in the range 0 to 2<img src="/tex/f30fdded685c83b0e7b446aa9c9aa120.svg?invert_in_darkmode&sanitize=true" align=middle width=9.96010619999999pt height=14.15524440000002pt/>.

## Himmelblau function

The Himmelblau function is defined by <img src="/tex/ba8b638e550005abe23a2205683ba34e.svg?invert_in_darkmode&sanitize=true" align=middle width=285.31931999999995pt height=26.76175259999998pt/>.
It has 4 minima:
* (-2.81, 3.13)
* (-3, 2)
* (3.58, -1.85)
* (3, 2)

To obtain the above minima, use seed=1, seed=7, seed=3, seed=4, respectively, for 10 particles.

10 particles, 50 iterations, c1=1, c2=1, W=0.5

<img src="https://github.com/nikhilkmr300/pso_solver/blob/master/images/himmelblau_1.png" width="320" height="240"><img src="https://github.com/nikhilkmr300/pso_solver/blob/master/images/himmelblau_3.png" width="320" height="240">
<img src="https://github.com/nikhilkmr300/pso_solver/blob/master/images/himmelblau_4.png" width="320" height="240"><img src="https://github.com/nikhilkmr300/pso_solver/blob/master/images/himmelblau_7.png" width="320" height="240">

Particles approaching each of the 4 minima of the Himmelblau function.

Reference: https://en.wikipedia.org/wiki/Himmelblau%27s_function

# Installation
Install `pip` if you do not have it already. Refer https://pip.pypa.io/en/stable/installing/.
Use the command `pip install pso-solver` to install the package.

# Description of functions
Here is a description of the functions that you might want to use in your code:
* createParticleList: Takes a list of initial positions and returns a list of particles in particleList initialized to those positions.
pBestPos of each particle is initialized to position passed in the list.
* createRandomParticleList: Returns a list of particles with randomly initialized positions.
* pso: Finds minimum or maximum (set maxFlag to True) of function f using the PSO algorithm.
* psoVisualizeUnivariate: Finds minimum or maximum (set maxFlag to True) of function f of 1 variable using the PSO algorithm and provides a nice visualization of the motion of the particles.
* psoVisualizeBivariate: Finds minimum or maximum (set maxFlag to True) of function f of 2 variables using the PSO algorithm and provides a nice visualization of the motion of the particles.
* setSeed: Sets seed for random number generators.
Use this function to set the seed in your program before calling any function that uses a PRNG if you want to get reproducible results.

Documentation is part of the source code file as PEP8 comments.

The tests directory in this repository contains some code you might find useful in understanding how to use this package.
