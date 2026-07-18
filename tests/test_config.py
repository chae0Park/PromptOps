from app.core.config import settings


def test_settings():

    assert settings.openai_api_key != ""
    assert settings.openai_model != ""