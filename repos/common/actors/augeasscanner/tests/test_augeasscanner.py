from leapp.snactor.fixture import current_actor_context
from leapp.models import AugeasOutput


def test_no_input_execution(current_actor_context):
    # test actor without consuming a message - empty output message is expected

    current_actor_context.run()

    output = current_actor_context.consume(AugeasOutput)

    # only one message has to be produced when no input is provided
    assert len(output) == 1

    output = output[0]

    # the only field has to be empty list
    assert output.items == []
