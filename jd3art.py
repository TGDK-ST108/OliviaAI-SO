import os
import json
import torch
import torch.nn as nn
import numpy as np
from datetime import datetime
from tokenizers import ByteLevelBPETokenizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from multiprocessing import Pool
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.tensorboard import SummaryWriter

# Define the custom neural layer
class CustomLayer(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(CustomLayer, self).__init__()
        self.fc = nn.Linear(input_dim, output_dim)
        self.activation = nn.ReLU()

    def forward(self, x):
        x = self.fc(x)
        return self.activation(x)

class PhaseAwareCustomLayer(nn.Module):
    def __init__(self, input_dim, output_dim, num_phases):
        super(PhaseAwareCustomLayer, self).__init__()
        self.phase_embedding = nn.Embedding(num_phases, input_dim)
        self.fc = nn.Linear(input_dim, output_dim)
        self.activation = nn.ReLU()

    def forward(self, x, phase_id):
        phase_embed = self.phase_embedding(phase_id)
        x = x + phase_embed  # Incorporating phase information
        x = self.fc(x)
        return self.activation(x)

class ModifiedModel(nn.Module):
    def __init__(self, base_model, custom_layer, enable_custom_layer=True):
        super(ModifiedModel, self).__init__()
        self.base_model = base_model
        self.custom_layer = custom_layer
        self.enable_custom_layer = enable_custom_layer

    def forward(self, input_data):
        base_output = self.base_model(input_data)
        if self.enable_custom_layer:
            return self.custom_layer(base_output)
        return base_output

class DynamicStory:
    def __init__(self):
        self.fragments = []

    def add_fragment(self, fragment):
        self.fragments.append(fragment)

    def build_narrative(self, current_events):
        story = f"Current events on {datetime.now().strftime('%Y-%m-%d')}:\n"
        story += " ".join(current_events) + "\n\n"
        for fragment in self.fragments:
            story += fragment.generate() + "\n"
        return story

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
            special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>"]
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

        print(f"Tokenizer and configuration files created in {tokenizer_dir}.")

    def train_model(base_model, custom_layer, data_loader, num_epochs):
        model = ModifiedModel(base_model, custom_layer)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=10)

        writer = SummaryWriter("./logs")

        for epoch in range(num_epochs):
            model.train()
            total_loss = 0
            for batch in data_loader:
                optimizer.zero_grad()
                inputs, labels = batch
                outputs = model(inputs)
                loss = nn.CrossEntropyLoss()(outputs, labels)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
 
            avg_loss = total_loss / len(data_loader)
            writer.add_scalar("Loss", avg_loss, epoch)
            scheduler.step(avg_loss)

            print(f"Epoch {epoch+1}/{num_epochs}, Loss: {avg_loss}")

        writer.close()
        return model

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

if __name__ == "__main__":
    setup_directories_and_files()

    # Example base model (simple feedforward for demonstration purposes)
    class BaseModel(nn.Module):
        def __init__(self, input_dim, hidden_dim, output_dim):
            super(BaseModel, self).__init__()
            self.fc1 = nn.Linear(input_dim, hidden_dim)
            self.activation = nn.ReLU()
            self.fc2 = nn.Linear(hidden_dim, output_dim)

        def forward(self, x):
            x = self.activation(self.fc1(x))
            return self.fc2(x)

    input_dim = 768
    hidden_dim = 256
    output_dim = 10
    base_model = BaseModel(input_dim, hidden_dim, output_dim)

    custom_layer = CustomLayer(output_dim, 128)
    dummy_data = [
        (torch.randn(32, input_dim), torch.randint(0, output_dim, (32,)))
        for _ in range(100)
    ]
    data_loader = torch.utils.data.DataLoader(dummy_data, batch_size=8)

    trained_model = train_model(base_model, custom_layer, data_loader, num_epochs=5)

    # Generate a dynamic story
    current_events = [
        "The rise of AI sparks philosophical debates.",
        "Environmental movements gain momentum.",
        "The world reflects on the importance of compassion and strength."
    ]

    story_builder = DynamicStory()
    fragments = [
        StoryFragment("Lincoln", "honor and unity", "The Wise Leader", ["standing for justice", "bridging divided communities"]),
        StoryFragment("Vajrayogini", "wisdom and compassion", "The Enlightened Warrior", ["facing internal struggles", "offering transformation"]),
    ]

    for frag in fragments:
        story_builder.add_fragment(frag)

    narrative = story_builder.build_narrative(current_events)
    print(narrative)
