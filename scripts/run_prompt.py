from app.services.prompt_loader import load_prompt
from app.services.prompt_runner import PromptRunner

prompt = load_prompt("customer_support_v1.json")

runner = PromptRunner()

response = runner.run(
    prompt,
    "How can I reset my password?"
)

print(response)