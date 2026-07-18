from app.services.prompt_loader import load_prompt


def test_load_prompt():

    prompt = load_prompt("customer_support_v1.json")

    assert prompt.name == "customer-support"
    assert prompt.version == "v1"
    assert (
        prompt.system_prompt
        == "You are a helpful customer support assistant."
    )