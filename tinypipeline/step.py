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
    name: str,
    version: str,
    description: str,
    callable: Callable = None,
):
    """
    Create a step for a pipeline. Can be used as a decorator or a function.

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
    if callable is not None:
        print(
            f"WARNING: step() is being used as a function for {name}. "
            "This is deprecated and will be removed in a future version. "
            "Please use step() as a decorator instead."
        )

        _step = Step(
            callable=callable,
            name=name,
            version=version,
            description=description,
        )
        return _step
    
    def decorator(callable):
        _step = Step(
            callable=callable,
            name=name,
            version=version,
            description=description,
        )
        return _step
    return decorator
