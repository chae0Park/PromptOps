from app.services.golden_set_loader import load_golden_set


def test_load_golden_set():
    dataset = load_golden_set("customer_support.json")

    assert len(dataset) == 2
    assert dataset[0].input == "How can I reset my password?"
    assert (
        dataset[0].expected_output
        == "Go to the login page and select Forgot Password."
    )