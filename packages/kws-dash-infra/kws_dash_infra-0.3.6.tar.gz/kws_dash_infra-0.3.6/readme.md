# A Dash Infrastructure Framework

## Quickstart

### Architecture of an application

![architecture](docs/imgs/archi.svg)

## Introduction

This package defines a standard framework for the development of Dash Applications, both in the context of prototyping and production applications. 

The core idea of this framework is to separate **core logic** from **display and interaction elements**.

The framework relies on several core concepts, which are the building blocks of an application.

- [Callbacks](#Callbacks) are an abstraction for Dash Apps function.
  They perform the conversion between the Dash inputs, the core function and the Dash outputs.
  Therefore a callback should at least be composed of a `_pre_function_hook` and a `_post_function_hook`, wrapping a function representing the core functionality.
- [Components](#Components) are an abstraction for Dash components.
  A Component is an object which has self contained Dash callbacks.
  Those callbacks should only operate on the functionality of the Component, but have no meaningful functionality.
  For instance, the `StoreComponent` has a callback to store the outputs from an another Callback into its state.
- [Dash Apps](#Dash-Apps) are an abstraction for Dash standard Application.
  A Dash Application has one or multiple `Component`s, and `Callback`s.
- [Super Apps](#Super-Apps) are a grouping of multiple `DashApp`s inside a global application.
  Super apps expose an API for every core Callback registered inside it.

In addition to this framework, this package adds a few helper classes, such as a `StoreComponent` or a `FigureComponent`.

## Core Concepts

### Callbacks

#### Example

```python
# callbacks.py
from dash_infra import as_callback
import numpy as np

def to_linspace(state, num_points):
    # A hook function takes the state of the callback as a first argument

    return np.linspace(0, 100, num_points)

def to_figure(state, array: np.ndarray):
    return {"data": [dict(x=state.current_inputs[0], y=outputs, mode="markers")]}


@as_callback(                           # Changes the function into an unbound callback
    NumpySerializer,                    # Mixins adds capabilities to the callback
    pre_func_hooks=[to_linspace],       # Takes the input and changes it into a np.array
    post_func_hooks=[to_figure],        # Takes the output and converts it into a plotly graph
)
def square(x: "Arrayable") -> np.ndarray:
    """
    Computes the square of an array x
    """
    # the function is defined as it would normally be
    return np.array(x) ** 2

```

At this point the callback `square` is not bound to any app or inputs.
It is still a callable, and `square([1,2,3])` returns `[1, 4, 9]`.

### Components

#### Example

```python
# components.py
from dash_core_components import Graph, Slider

from dash_infra import as_component
from dash_infra.components.groups import ComponentGroup
from dash_infra.html_helpers.divs import Col


graph_square = as_component(Graph, "square", container=Col(s=6))
slider = as_component(Slider, "input", container=Col(s=6))
group = ComponentGroup("main", slider, graph_square, graph_cube)

```

Standard dash components can be transferred into our framework with `as_component(obj, id, container)`.
This conversion allows easier registry in the Dash application

### Dash Apps

#### Example

```python
# app.py

from dash_infra import KWSDashApp
from .components import group
from .callbacks import square

dash_app = KWSDashApp("A multplier component", doc=__doc__)
dash_app.register_component(group)
dash_app.register_callback(
    square, 
    outputs=("square", "figure"), 
    inputs=[("input", "value")]
)

```

### Super Apps

Super apps wrap Dash apps, and provide the Dash callbacks with a restful API.

### Stores

Store Components are an abstraction used to store callback outputs for later usage. Store contents are available for all callbacks to use.

![stores](docs/imgs/store.svg)
