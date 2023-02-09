from typing import Callable


class Step:
    def __init__(
        self,
        callable: Callable,
        name: str,
        version: str,
        description: str,
    ) -> None:
        """
        A step is a single unit of work in a pipeline.

        Params
        ------
        callable: Callable
            The function that is called when the step is run.
        name: str
            The name of the step.
        version: str
            The version of the step.
        description: str
            A description of the step.
        """
        self._callable = callable
        self.name = name
        self.version = version
        self.description = description

    def run(self):
        """
        Run the step.
        """
        self._callable()
        return None


def step(
    callable: Callable,
    name: str,
    version: str,
    description: str,
):
    """
    Create a step for a pipeline.

    Params
    ------
    callable: Callable
        The function that is called when the step is run.
    name: str
        The name of the step.
    version: str
        The version of the step.
    description: str
        A description of the step.
    """
    _step = Step(
        callable=callable,
        name=name,
        version=version,
        description=description,
    )
    return _step
