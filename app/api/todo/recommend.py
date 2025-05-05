# app/api/recommend/recommend.py
import random
import re
import dspy
from dspy import LM
from app.core import config

# Step 1: Configure DSPy Language Model
lm = LM(
    "azure/gpt-4o",
    api_key=config.AZURE_OPENAI_API_KEY,
    api_base=config.AZURE_OPENAI_ENDPOINT,
    api_version=config.AZURE_OPENAI_API_VERSION,
)

dspy.settings.configure(lm=lm)

# Step 2: Define Signature
class TodoRecommendations(dspy.Signature):
    theme = dspy.InputField(desc="Focus area for task ideas")
    recommendations = dspy.OutputField(desc="JSON object with task suggestions")

# Step 3: Predictor Instance
generate = dspy.Predict(TodoRecommendations)

# Step 4: Prompts
PROMPTS = [
    "Suggest 5 productive to-do tasks for someone working from home as a software developer. Keep them concise, actionable, and clear.",
    "List 5 daily goals a remote frontend engineer should try to accomplish to stay productive.",
    "Give me 5 helpful daily habits for a backend developer to maximize productivity while working remotely.",
    "Suggest 5 important work-from-home tasks a full-stack developer should complete each day.",
    "List 5 small, focused tasks for a software developer working remotely to boost efficiency and mental clarity."
]

# Step 5: Core function to generate recommendation
async def generate_recommendations_dspy():
    prompt = random.choice(PROMPTS)
    response = lm.forward(prompt)
    raw = response['choices'][0]['message']['content']

    # Extract numbered items (e.g., 1. ..., 2. ...)
    items = re.split(r'\n?\d+\.\s+', raw.strip())
    structured_recommendations = []

    for item in items:
        if not item.strip():
            continue
        # Split title and description by the first colon
        if ':' in item:
            title, description = item.split(':', 1)
            structured_recommendations.append({
                "title": title.strip(" *"),
                "description": description.strip()
            })
        else:
            # fallback if colon is missing
            structured_recommendations.append({
                "title": item.strip(" *"),
                "description": ""
            })

    return {"recommendations": structured_recommendations}

