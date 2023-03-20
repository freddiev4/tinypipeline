import functools

from datetime import datetime
from graphlib import CycleError, TopologicalSorter
from typing import Callable, Union, Dict, List

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

    @functools.cached_property
    def steps(self) -> Union[List[Step], Dict[Step, Step]]:
        """
        The steps for the pipeline. Cached property so that the function
        containing the steps is only called once.

        Returns
        -------
        Union[List[Step], Dict[Step, Step]]
            The steps for the pipeline.
        """
        return self._func()

    @property
    def ordering(self) -> str:
        """
        The ordering of the steps in the pipeline. Either linear or nonlinear.

        Returns
        -------
        str
            'linear' or 'nonlinear'.
        """
        if isinstance(self.steps, List):
            _ordering = 'linear'
        elif isinstance(self.steps, Dict):
            _ordering = 'nonlinear'
        else:
            raise TypeError("Pipeline steps must be in a list or a dict.")

        return _ordering

    def __repr__(self):
        """
        Representation of the pipeline.
        """
        return f"Pipeline(name='{self.name}', version='{self.version}')"

    def _get_steps(self):
        """
        Private method to order the steps for the pipeline.

        Uses `self.steps` if the ordering is linear (a list of steps)
        and uses a reversed topological sort on `self.steps` if the ordering
        is nonlinear (a dictionary).
        """
        # if the steps are in a list, just return them in order
        # in which they were defined
        if self.ordering == 'linear':
            _steps = self.steps

        # if the steps are in a dictionary, return them in a topologically
        # sorted order, based on the dependencies defined in the dictionary.
        # then reverse the order since keys in the dictionary are the steps
        # and values are the dependencies.
        elif self.ordering == 'nonlinear':
            ts = TopologicalSorter(graph=self.steps)
            toposorted_steps = list(ts.static_order())
            _steps = list(reversed(toposorted_steps))

        if not all(isinstance(s, Step) for s in self.steps):
            raise TypeError(
                "Not a valid step. Consider using the step decorator "
                "to create steps for your pipeline."
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

        # run steps in linear or nonlinear order depending
        # on the ordering property of the pipeline
        try:
            step_order = self._get_steps()
        except CycleError:
            print(
                "Pipeline failed due to an exception in step ordering. "
                "Try checking for circular dependencies in your steps.\n"
            )
            raise

        for step in step_order:
            try:
                print(f"Running step [{step.name}]...")

                start = datetime.now()
                step.run()
                end = datetime.now()

                completion_time = (end - start).total_seconds()
                print(f"Step [{step.name}] completed in {completion_time} seconds\n")
            except Exception:
                print(f"Pipeline failed due to an exception in step [{step.name}]")
                raise


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
                    "The pipeline decorator only accepts functions. "
                    f"Passed {type(func)}"
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
