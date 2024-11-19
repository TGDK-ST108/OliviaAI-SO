import os
import json
import torch
import torch.nn as nn
import numpy as np
from datetime import datetime
from tokenizers import ByteLevelBPETokenizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, PretrainedConfig
from transformers import Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Define the custom neural layer
class CustomLayer(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(CustomLayer, self).__init__()
        self.fc = nn.Linear(input_dim, output_dim)
        self.activation = nn.ReLU()

    def forward(self, x):
        x = self.fc(x)
        return self.activation(x)

# Define the combined model
class ModifiedModel(nn.Module):
    def __init__(self, base_model, custom_layer):
        super(ModifiedModel, self).__init__()
        self.base_model = base_model
        self.custom_layer = custom_layer

    def forward(self, input_ids, attention_mask=None, labels=None):
        base_output = self.base_model(input_ids, attention_mask=attention_mask)
        custom_output = self.custom_layer(base_output.logits)
        return custom_output

# Define storytelling components
class StoryFragment:
    def __init__(self, name, theme, archetype, elements):
        self.name = name
        self.theme = theme
        self.archetype = archetype
        self.elements = elements

    def generate(self):
        fragment = f"{self.name}: {self.archetype} embodies {self.theme}. "
        for element in self.elements:
            fragment += f"{element}. "
        return fragment

class Duofragment:
    def __init__(self, fragment1, fragment2):
        self.fragment1 = fragment1
        self.fragment2 = fragment2

    def combine(self):
        return f"{self.fragment1.generate()} Meanwhile, {self.fragment2.generate()}"

class DynamicStory:
    def __init__(self):
        self.fragments = []

    def add_fragment(self, fragment):
        self.fragments.append(fragment)

    def build_narrative(self, current_events):
        story = f"Current events on {datetime.now().strftime('%Y-%m-%d')}:\n"
        story += " ".join(current_events) + "\n\n"
        story += "Form is emptiness. Emptiness is form. Form is not other than emptiness. Emptiness is not other than form.\n\n"
        for fragment in self.fragments:
            story += fragment.generate() + "\n"
        return story

def setup_directories_and_files():
    tokenizer_dir = "./OliviaAI"
    os.makedirs(tokenizer_dir, exist_ok=True)

    # Check and generate `custom_dataset.txt` if missing
    dataset_path = os.path.join(os.getcwd(), "custom_dataset.txt")
    if not os.path.exists(dataset_path):
        print(f"File {dataset_path} not found. Generating a sample dataset...")
        with open(dataset_path, "w") as f:
            f.write("This is a sample sentence for training the tokenizer.\n")
            f.write("Another example sentence for testing the custom tokenizer.\n")
        print(f"Sample dataset created at {dataset_path}.")

    # Train and save tokenizer
    tokenizer = ByteLevelBPETokenizer()
    tokenizer.train(
        files=[dataset_path],
        vocab_size=30000,
        min_frequency=2,
        special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>", "<Gentuo>", "<warden_vector>"]
    )
    tokenizer.save_model(tokenizer_dir)

    # Save tokenizer configuration
    tokenizer_config = {
        "do_lower_case": False,
        "unk_token": "<unk>",
        "bos_token": "<s>",
        "eos_token": "</s>",
        "pad_token": "<pad>",
        "mask_token": "<mask>"
    }
    with open(os.path.join(tokenizer_dir, "tokenizer_config.json"), "w") as f:
        json.dump(tokenizer_config, f)

    # Ensure `config.json` includes `model_type`
    config_path = os.path.join(tokenizer_dir, "config.json")
    if not os.path.exists(config_path) or not validate_config(config_path):
        model_config = {
            "model_type": "bert",  # Explicitly set the model type
            "vocab_size": 30000,
            "hidden_size": 768,
            "num_attention_heads": 12,
            "num_hidden_layers": 12,
            "pad_token_id": 0
        }
        with open(config_path, "w") as f:
            json.dump(model_config, f)
        print(f"Model configuration saved at {config_path}.")


# Validate config.json
def validate_config(config_path):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return "model_type" in config and bool(config["model_type"])
    except Exception as e:
        print(f"Error validating config.json: {e}")
        return False


# Setup tokenizer and model
def setup_tokenizer_and_model():
    tokenizer_dir = "./OliviaAI"
    
    # Validate the config.json before loading
    config_path = os.path.join(tokenizer_dir, "config.json")
    if not validate_config(config_path):
        raise ValueError(f"Invalid or missing config.json in {tokenizer_dir}. Run setup_directories_and_files() first.")

    # Load tokenizer and model
    auto_tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
    base_model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=10
    )
    return auto_tokenizer, base_model

# Create symbolic archetypes and themes
def create_gentuo_fragments():
    lincoln_fragment = StoryFragment(
        name="Lincoln",
        theme="honor and unity",
        archetype="The Wise Leader",
        elements=["standing for justice and equality", "bridging divided communities"]
    )
    vajrayogini_fragment = StoryFragment(
        name="Vajrayogini",
        theme="wisdom and compassion",
        archetype="The Enlightened Warrior",
        elements=["facing internal struggles", "offering a path of transformation"]
    )
    vajrapani_fragment = StoryFragment(
        name="Vajrapani",
        theme="strength and determination",
        archetype="The Protector",
        elements=["facing external chaos", "defending the innocent"]
    )
    duofragment = Duofragment(vajrayogini_fragment, vajrapani_fragment)

    freya_fragment = StoryFragment(
        name="Freya",
        theme="love, fertility, and battle",
        archetype="The Norse Goddess",
        elements=["empowering others in love and war", "bridging connections between realms"]
    )
    tara_fragment = StoryFragment(
        name="Tara",
        theme="compassion and healing",
        archetype="The Divine Savior",
        elements=["guiding the lost", "offering healing to the wounded"]
    )
    padmasambhava_fragment = StoryFragment(
        name="Padmasambhava",
        theme="spiritual awakening and magic",
        archetype="The Guru",
        elements=["revealing hidden truths", "connecting the material and spiritual worlds"]
    )

    return [lincoln_fragment, duofragment, freya_fragment, tara_fragment, padmasambhava_fragment]

def setup_directories_and_files():
    tokenizer_dir = "./OliviaAI"
    os.makedirs(tokenizer_dir, exist_ok=True)

    # Check and generate `custom_dataset.txt` if missing
    dataset_path = os.path.join(os.getcwd(), "custom_dataset.txt")
    if not os.path.exists(dataset_path):
        print(f"File {dataset_path} not found. Generating a sample dataset...")
        with open(dataset_path, "w") as f:
            f.write("This is a sample sentence for training the tokenizer.\n")
            f.write("Another example sentence for testing the custom tokenizer.\n")
        print(f"Sample dataset created at {dataset_path}.")

    # Train and save tokenizer
    tokenizer = ByteLevelBPETokenizer()
    tokenizer.train(
        files=[dataset_path],
        vocab_size=30000,
        min_frequency=2,
        special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>", "<Gentuo>", "<warden_vector>"]
    )
    tokenizer.save_model(tokenizer_dir)

    # Create tokenizer configuration
    tokenizer_config = {
        "do_lower_case": False,
        "unk_token": "<unk>",
        "bos_token": "<s>",
        "eos_token": "</s>",
        "pad_token": "<pad>",
        "mask_token": "<mask>"
    }
    with open(os.path.join(tokenizer_dir, "tokenizer_config.json"), "w") as f:
        json.dump(tokenizer_config, f)

    # Create model configuration
    model_config = PretrainedConfig(
        model_type="bert",
        vocab_size=30000,
        hidden_size=768,
        num_attention_heads=12,
        num_hidden_layers=12,
        pad_token_id=0
    )
    with open(os.path.join(tokenizer_dir, "config.json"), "w") as f:
        json.dump(model_config.to_dict(), f)

    print(f"Tokenizer and configuration files created in {tokenizer_dir}.")

# Main execution
if __name__ == "__main__":
    setup_directories_and_files()

    # Setup tokenizer and model
    tokenizer, base_model = setup_tokenizer_and_model()


    input_dim = base_model.config.hidden_size
    output_dim = 128
    custom_layer = CustomLayer(input_dim, output_dim)

    modified_model = ModifiedModel(base_model, custom_layer)
    torch.save(modified_model.state_dict(), "./modified_model/OliviaAI.pth")

    current_events = [
        "The rise of AI sparks philosophical debates.",
        "Environmental movements gain momentum.",
        "The world reflects on the importance of compassion and strength."
    ]

    story_builder = DynamicStory()
    fragments = create_gentuo_fragments()

    for frag in fragments:
        story_builder.add_fragment(frag)

    narrative = story_builder.build_narrative(current_events)
    print(narrative)