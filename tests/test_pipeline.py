from unittest.mock import Mock, call

import pytest

from tinypipeline import pipeline, step


def test_pipeline_completion():
    """
    Test that the pipeline runs all the steps in the correct order.
    """
    mock_step_1 = Mock()
    mock_step_2 = Mock()
    mock_step_3 = Mock()

    mock_step_1.return_value = "step 1"
    mock_step_2.return_value = "step 2"
    mock_step_3.return_value = "step 3"

    @pipeline(
        name="test_pipeline",
        description="Test pipeline",
        version="1.0.0",
    )
    def test_pipeline():
        step_one = step(
            callable=mock_step_1,
            name="step_one",
            description="Step one",
            version="1.0.0",
        )

        step_two = step(
            callable=mock_step_2,
            name="step_two",
            description="Step two",
            version="1.0.0",
        )

        step_three = step(
            callable=mock_step_3,
            name="step_three",
            description="Step three",
            version="1.0.0",
        )

        return [step_one, step_two, step_three]

    pipe = test_pipeline()
    pipe.run()

    assert len(pipe.steps) == 3
    mock_step_1.assert_called_once()
    mock_step_2.assert_called_once()
    mock_step_3.assert_called_once()

def test_pipeline_completion_using_step_decorator():
    """
    Test that the pipeline runs all the steps in the correct order,
    using the step decorator instead of the step function.
    """
    mock_step_1 = Mock()
    mock_step_2 = Mock()
    mock_step_3 = Mock()

    mock_step_1.return_value = "step 1"
    mock_step_2.return_value = "step 2"
    mock_step_3.return_value = "step 3"

    @step(
        name="step_one",
        description="Step one",
        version="1.0.0",
    )
    def step_one():
        mock_step_1()

    @step(
        name="step_two",
        description="Step two",
        version="1.0.0",
    )
    def step_two():
        mock_step_2()

    @step(
        name="step_three",
        description="Step three",
        version="1.0.0",
    )
    def step_three():
        mock_step_3()

    @pipeline(
        name="test_pipeline",
        description="Test pipeline",
        version="1.0.0",
    )
    def test_pipeline():
        return [step_one, step_two, step_three]

    pipe = test_pipeline()
    pipe.run()

    assert len(pipe.steps) == 3
    mock_step_1.assert_called_once()
    mock_step_2.assert_called_once()
    mock_step_3.assert_called_once()


def test_pipeline_completion_with_dict_ordering():
    """
    Test that the pipeline runs all the steps in the correct order,
    defined by a dictionary that has the steps as keys and the steps
    that depend on them as values.

    Ensure the topological ordering is correct.
    """
    mock_step_1 = Mock()
    mock_step_2 = Mock()
    mock_step_3 = Mock()
    mock_step_4 = Mock()
    mock_step_5 = Mock()

    mock_step_1.return_value = "step 1"
    mock_step_2.return_value = "step 2"
    mock_step_3.return_value = "step 3"
    mock_step_4.return_value = "step 4"
    mock_step_5.return_value = "step 5"

    # set up a mock manager to track the calls to the steps
    mock_manager = Mock()
    mock_manager.attach_mock(mock_step_1, "step_one")
    mock_manager.attach_mock(mock_step_2, "step_two")
    mock_manager.attach_mock(mock_step_3, "step_three")
    mock_manager.attach_mock(mock_step_4, "step_four")
    mock_manager.attach_mock(mock_step_5, "step_five")

    @step(name="step_one", description="Step one", version="1.0.0")
    def step_one():
        mock_step_1()

    @step(name="step_two", description="Step two", version="1.0.0")
    def step_two():
        mock_step_2()

    @step(name="step_three", description="Step three", version="1.0.0")
    def step_three():
        mock_step_3()

    @step(name="step_four", description="Step four", version="1.0.0")
    def step_four():
        mock_step_4()

    @step(name="step_five", description="Step five", version="1.0.0")
    def step_five():
        mock_step_5()

    @pipeline(
        name="test_pipeline",
        description="Test pipeline",
        version="1.0.0",
    )
    def test_pipeline():
        """
        Run the steps in the following order:
        step_five -> step_two -> step_three -> step_four -> step_one
        """
        return {
            step_five: [step_two],
            step_two: [step_three],
            step_three: [step_four, step_one],
            step_four: [step_one],
        }

    pipe = test_pipeline()
    pipe.run()

    steps = []
    for key, value in pipe.steps.items():
        steps.append(key)
        steps.extend(value)

    steps = set(steps)

    # check that the number of steps is correct
    assert len(steps) == 5

    # check that all of the steps were called in a particular order
    # using the mock manager
    expected_calls = [
        call.step_five(),
        call.step_two(),
        call.step_three(),
        call.step_four(),
        call.step_one(),
    ]

    assert mock_manager.mock_calls == expected_calls

def test_pipeline_failure_no_function_passed():
    """
    Test that the pipeline fails with a TypeError if no function is passed
    to the method.

    Also check that the error message is correct.
    """
    data = ""
    with pytest.raises(TypeError) as context:
        pipe = pipeline(
            name="test_pipeline",
            description="Test pipeline",
            version="1.0.0",
        )
        pipe(data)().run()

    assert (
        f"The pipeline decorator only accepts functions. Passed {type(data)}"
        == str(context.value)
    )

def test_pipeline_failure_invalid_step():
    """
    Test that the pipeline fails with a TypeError if there is no instance of Step,
    in a list of pipeline steps.

    Also check that the error message is correct.
    """

    @pipeline(
        name="test_pipeline",
        description="Test pipeline",
        version="1.0.0",
    )
    def test_pipeline():
        return ["step_one"]

    with pytest.raises(TypeError) as context:
        pipe = test_pipeline()
        pipe.run()

    assert (
        "Not a valid step. Consider using the step decorator to "
        "create steps for your pipeline."
        == str(context.value)
    )

def test_pipeline_failure_no_steps_list_or_dict():
    """
    Test that the pipeline fails with a TypeError if there are no
    steps in a list or a dictionary.

    Also check that the error message is correct.
    """
    # create step one
    @step(
        name="step_one",
        description="Step one",
        version="1.0.0",
    )
    def step_one():
        pass


    @pipeline(
        name="test_pipeline",
        description="Test pipeline",
        version="1.0.0",
    )
    def test_pipeline():
        return step_one

    with pytest.raises(TypeError) as context:
        pipe = test_pipeline()
        pipe.run()

    assert "Pipeline steps must be in a list or a dict." == str(context.value)

def test_pipeline_failure_no_steps_to_run():
    """
    Test that the pipeline fails with an Exception if there are no steps to run.

    Also check that the error message is correct.
    """

    @pipeline(
        name="test_pipeline",
        description="Test pipeline",
        version="1.0.0",
    )
    def test_pipeline():
        return []

    with pytest.raises(Exception) as context:
        pipe = test_pipeline()
        pipe.run()

    assert f"Pipeline {pipe.name} has no steps to run." == str(context.value)

def test_pipeline_failure_exception_in_step():
    """
    Test that the pipeline fails with an Exception if there is an exception
    in one of the steps.

    Also check that the error message is correct.
    """
    mock_step_1 = Mock()
    mock_step_2 = Mock()
    mock_step_3 = Mock()

    mock_step_1.return_value = "step 1"
    mock_step_2.side_effect = Exception("Something went wrong")
    mock_step_3.return_value = "step 3"

    @pipeline(
        name="test_pipeline",
        description="Test pipeline",
        version="1.0.0",
    )
    def test_pipeline():
        step_one = step(
            callable=mock_step_1,
            name="step_one",
            description="Step one",
            version="1.0.0",
        )

        step_two = step(
            callable=mock_step_2,
            name="step_two",
            description="Step two",
            version="1.0.0",
        )

        step_three = step(
            callable=mock_step_3,
            name="step_three",
            description="Step three",
            version="1.0.0",
        )

        return [step_one, step_two, step_three]

    with pytest.raises(Exception) as context:
        pipe = test_pipeline()
        pipe.run()

    assert str(mock_step_2.side_effect) == str(context.value)
