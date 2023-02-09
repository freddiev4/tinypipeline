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
- `step`: a function that is used to define individual pipeline steps. Returns a `Step` instance.

Each object requires you provide a `name`, `version`, and `description` to explicitly define what pipeline you're creating.

The `Pipeline` object that is returned from the decorator has a single method: `run()`.

## API

If you'd like to use this package, you can follow the `example.py` below:

```python
from tinypipeline import pipeline, step


def step_fn_one():
    print("Step function one")

def step_fn_two():
    print("Step function two")

@pipeline(
    name='test-pipeline', 
    version='0.0.1', 
    description='a test tinypipeline',
)
def pipe():
    step_one = step(
        callable=step_fn_one, 
        name='step_one', 
        version='0.0.1', 
        description='first step',
    )
    step_two = step(
        name='step_two',
        version='0.0.1',
        description='second step',
        callable=step_fn_two,
    )
    return [step_one, step_two]

pipe = pipe()
pipe.run()
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
Step [step_one] completed in 0.000356 seconds

Running step [step_two]...
Step function two
Step [step_two] completed in 0.000317 seconds
```

## Running tests

Tests are run using pytest. To run the tests you can do:

```console
$ pip install pytest
$ pytest
```

## Limitations

- Currently `tinypipeline` only supports linear pipelines, and doesn't support full dependency graphs