# diffeqtorch

Bridges `DifferentialEquations.jl` with PyTorch. Besides benefitting from the huge range of solvers available in `DifferentialEquations.jl`, this allows taking gradients through solvers using [local sensitivity analysis/auto-diff](https://docs.sciml.ai/stable/analysis/sensitivity/). The package has only been tested with ODE problems, and in particular, automatic differentiation is only supported for ODEs using `ForwardDiff.jl`. This can be extended in the future, [contributions are welcome](CONTRIBUTING.md).


### Examples

- [Simple ODE problem to demonstrate the interface and confirm gradients with analytical solution](https://github.com/jan-matthis/diffeqtorch/blob/master/notebooks/01_simple_ode.ipynb)
- [SIR model for a slighlty more complicated model with numerical gradient checking](https://github.com/jan-matthis/diffeqtorch/blob/master/notebooks/02_sir_model.ipynb)
- [Hodgkin-Huxley model for a realistic example from Neuroscience](https://github.com/jan-matthis/diffeqtorch/blob/master/notebooks/03_hh_model.ipynb)


## Installation

Prerequisites for using `diffeqtorch` are installation of Julia and Python. Note that the binary directory of `julia` needs to be in your `PATH`.

We recommend using a custom Julia sytem image containing dependencies. If the environment variable `JULIA_SYSIMAGE_DIFFEQTORCH` is set, the installation script will automatically build the image. This may take a while but will improve speed afterwards.

Install `diffeqtorch`:
```commandline
$ export JULIA_SYSIMAGE_DIFFEQTORCH="$HOME/.julia_sysimage_diffeqtorch.so"
$ pip install diffeqtorch -v
```


## Usage

```python
from diffeqtorch import DiffEq

f = """
function f(du,u,p,t)
    du[1] = p[1] * u[1]
end
"""
de = DiffEq(f)

u0 = torch.tensor([1.])
tspan = torch.tensor([0., 3.])
p = torch.tensor([1.01])

u, t = de(u0, tspan, p)
```

See also `help(DiffEq)` and examples provided in `notebooks/`.


## License

MIT
