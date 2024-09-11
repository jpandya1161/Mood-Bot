import os
from path import current_dir
from rasa.core.agent import Agent
from functools import lru_cache

# Get the parent directory (moodbot_2 directory)
parent_dir = os.path.dirname(os.path.dirname(current_dir))

# Construct the path to the models directory
default_model_path = os.path.join(parent_dir, 'models', '20230703-155349-plain-race.tar.gz')


# Get the model path from the environment variable or use the default path
model_path = os.environ.get("model_path", default_model_path)

print("Model Path:", model_path)

@lru_cache(maxsize=None)

def load_rasa_model():
    # Verify if the model file exists at the specified path
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at path: {model_path}")

    # Load the Rasa model
    print("Model Path:", model_path)
    model = Agent.load(model_path)

    return model
