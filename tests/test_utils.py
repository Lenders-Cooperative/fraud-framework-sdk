import pytest

from fraud_framework_sdk import internal_utils


def test_user_agent():
    user_agent = internal_utils.get_user_agent()
    assert isinstance(user_agent, str)
    assert "fraud_framework_sdk" in user_agent  # check SDK client
    assert user_agent.startswith("Python")  # check no prefix


@pytest.mark.parametrize(
    "prefix,suffix",
    [("my-app", "suffix"), (12345, 123123123), ("!$^$", "#$#&$^&#"), (" ", " ")],
)
def test_user_agent_prefix_suffix(prefix, suffix):
    user_agent = internal_utils.get_user_agent(prefix=prefix, suffix=suffix)
    assert user_agent.startswith(str(prefix))
    assert user_agent.endswith(str(suffix))
