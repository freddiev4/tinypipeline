import functools

from datetime import datetime
from typing import Callable

from .step import Step


class Pipeline:
    def __init__(
        self,
        func: Callable,
        name: str,
        version: str,
        description: str,
    ) -> None:
        """
        A pipeline is a collection of steps that are run in order.

        Initialization of a pipeline is done via the pipeline decorator.

        Params
        ------
        func: Callable
            The function that returns the steps for the pipeline.
        name: str
            The name of the pipeline.
        version: str
            The version of the pipeline.
        description: str
            A description of the pipeline.
        """
        self._func = func

        self.name = name
        self.version = version
        self.description = description

        self.steps = self._get_steps()

    def __repr__(self):
        """
        Representation of the pipeline.
        """
        return f"Pipeline(name='{self.name}', version='{self.version}')"

    def _get_steps(self):
        """
        Private method to get the steps for the pipeline.
        """
        _steps = self._func()

        if not isinstance(_steps, list):
            raise TypeError("Pipeline steps must be in a list.")

        if not all(isinstance(s, Step) for s in _steps):
            raise TypeError(
                "Not a valid step. Consider using the step() method to create steps for your pipeline."
            )

        return _steps

    def run(self) -> None:
        """
        Run the pipeline steps in order and return None.

        Raises
        ------
        Exception
            If there is an exception in any of the steps.
        """
        if not self.steps or self.steps is None:
            raise Exception(f"Pipeline {self.name} has no steps to run.")

        border = f"+--------------------{len(str(self)) * '-'}+\n"
        header = f"{border}" f"| Running pipeline: {str(self)} |\n" f"{border}"
        print(header)

        for step in self.steps:
            try:
                print(f"Running step [{step.name}]...")

                start = datetime.now()
                step.run()
                end = datetime.now()

                completion_time = (end - start).total_seconds()
                print(f"Step [{step.name}] completed in {completion_time} seconds\n")
            except Exception as e:
                print(f"Pipeline failed due to an exception in step [{step.name}]")
                raise
        return None


def pipeline(
    *,
    name: str,
    version: str,
    description: str,
):
    """
    Decorator to create a pipeline.

    Params
    ------
    name: str
        The name of the pipeline.
    version: str
        The version of the pipeline.
    description: str
        A description of the pipeline.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            """
            Wrapper function for the pipeline decorator.
            """
            if not isinstance(func, Callable):
                raise TypeError(
                    f"The pipeline decorator only accepts functions. Passed {type(func)}"
                )

            _pipeline = Pipeline(
                func=func,
                name=name,
                version=version,
                description=description,
            )
            return _pipeline

        return wrapper

    return decorator
