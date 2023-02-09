from unittest.mock import Mock

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
        "Not a valid step. Consider using the step() method to create steps for your pipeline."
        == str(context.value)
    )

def test_pipeline_failure_no_steps_list():
    """
    Test that the pipeline fails with a TypeError if there is no list of steps.

    Also check that the error message is correct.
    """

    @pipeline(
        name="test_pipeline",
        description="Test pipeline",
        version="1.0.0",
    )
    def test_pipeline():
        return "step_one"

    with pytest.raises(TypeError) as context:
        pipe = test_pipeline()
        pipe.run()

    assert "Pipeline steps must be in a list." == str(context.value)

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
    Test that the pipeline fails with an Exception if there is an exception in one of the steps.

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
