# tinypipeline

## Overview

`tinypipeline` is a tiny mlops library that provides a simple framework for organizing your machine learning pipeline code into a series of steps. It does not handle networking, I/O, or compute resources. You do the rest in your pipeline steps.

## Installation

```
$ pip install tinypipeline
```

## Usage

`tinypipeline` exposes two main objects:
- `pipeline`: a decorator for defining your pipeline. Returns a `Pipeline` instance.
- `step`: a decorator that is used to define individual pipeline steps. Returns a `Step` instance.

Each object requires you provide a `name`, `version`, and `description` to explicitly define what pipeline you're creating.

The `Pipeline` object that is returned from the decorator has a single method: `run()`.

## API

If you'd like to use this package, you can follow the `example.py` below:

```python
from tinypipeline import pipeline, step

# define all of the steps
@step(name='step_one', version='0.0.1', description='first step')
def step_one():
    print("Step function one")

@step(name='step_two', version='0.0.1', description='second step')
def step_two():
    print("Step function two")

@step(name='step_three', version='0.0.1', description='third step')
def step_three():
    print("Step function three")

@step(name='step_four', version='0.0.1', description='fourth step')
def step_four():
    print("Step function four")


# define the pipeline
@pipeline(
    name='test-pipeline', 
    version='0.0.1', 
    description='a test tinypipeline',
)
def pipe():
    # run the steps in the defined order
    return [
        step_one, 
        step_two, 
        step_three, 
        step_four,
    ]

pipe = pipe()
pipe.run()
```

You can also define steps using a dictionary, where each key of the dictionary
is a step to run, and the values are steps that run after the step named in the key.

```python
# define the pipeline
@pipeline(
    name='test-pipeline', 
    version='0.0.1', 
    description='a test tinypipeline',
)
def pipe():
    # run the steps in the defined order of the graph
    return {
        step_one: [step_two, step_four],
        step_two: [step_three, step_four]
    }
```


**Output**:

You can run the `example.py` like so:

```console
$ python example.py
+-------------------------------------------------------------------+
| Running pipeline: Pipeline(name='test-pipeline', version='0.0.1') |
+-------------------------------------------------------------------+

Running step [step_one]...
Step function one
Step [step_one] completed in 0.000325 seconds

Running step [step_two]...
Step function two
Step [step_two] completed in 0.000286 seconds

Running step [step_three]...
Step function three
Step [step_three] completed in 0.000251 seconds

Running step [step_four]...
Step function four
Step [step_four] completed in 0.000313 seconds
```

## Running tests

Tests are run using pytest. To run the tests you can do:

```console
$ pip install pytest
$ pytest
```
