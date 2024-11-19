import os
import json
import pandas as pd
import torch
import torch.nn as nn
from datetime import datetime
from tokenizers import ByteLevelBPETokenizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from torch.utils.data import DataLoader, Dataset
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.tensorboard import SummaryWriter
from multiprocessing import Pool

# Define the custom neural layer
class CustomLayer(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(CustomLayer, self).__init__()
        self.fc = nn.Linear(input_dim, output_dim)
        self.activation = nn.ReLU()

    def forward(self, x):
        x = self.fc(x)
        return self.activation(x)

class QuantumLayer(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(QuantumLayer, self).__init__()
        self.fc1 = nn.Linear(input_dim, output_dim)
        self.fc2 = nn.Linear(output_dim, input_dim)
        self.activation = nn.Tanh()

    def forward(self, x):
        x = self.activation(self.fc1(x))
        x = self.fc2(x)
        return x

class ModifiedModel(nn.Module):
    def __init__(self, base_model, custom_layer, quantum_layer):
        super(ModifiedModel, self).__init__()
        self.base_model = base_model
        self.custom_layer = custom_layer
        self.quantum_layer = quantum_layer

    def forward(self, input_data):
        base_output = self.base_model(input_data)
        custom_output = self.custom_layer(base_output)
        quantum_output = self.quantum_layer(custom_output)
        return quantum_output

class CodeDataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_length):
        self.texts = dataframe['code'].tolist()
        self.labels = dataframe['label'].tolist()
        self.tokenizer = tokenizer
        self.max_length = max_length

        # Create a label mapping for string-to-integer conversion
        unique_labels = sorted(set(self.labels))
        self.label_to_id = {label: idx for idx, label in enumerate(unique_labels)}
        self.id_to_label = {idx: label for label, idx in self.label_to_id.items()}

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        try:
            # Tokenize the input text
            encoded = self.tokenizer.encode(self.texts[idx])
            input_ids = encoded.ids[:self.max_length]  # Truncate to max_length
            padding_length = self.max_length - len(input_ids)
            input_ids += [self.tokenizer.token_to_id("<pad>")] * padding_length  # Pad with <pad> tokens

            # Convert the label to its numeric ID
            label = self.label_to_id[self.labels[idx]]

            # Ensure proper data types for PyTorch tensors
            return torch.tensor(input_ids, dtype=torch.float32), torch.tensor(label, dtype=torch.long)

        except KeyError as e:
            raise ValueError(f"Error processing data at index {idx}: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error at index {idx}: {e}")



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

def setup_tokenizer_from_dataset(csv_path, tokenizer_dir):
    # Load dataset
    df = pd.read_csv(csv_path)
    if 'code' not in df.columns:
        raise ValueError("The dataset must have a 'code' column.")

    # Save text data to a temporary file
    dataset_path = os.path.join(tokenizer_dir, "temp_dataset.txt")
    df['code'].to_csv(dataset_path, index=False, header=False)

    # Train ByteLevelBPETokenizer
    tokenizer = ByteLevelBPETokenizer()
    tokenizer.train(
        files=[dataset_path],
        vocab_size=30000,
        min_frequency=2,
        special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>", "<Gentuo>"]
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
    return tokenizer

def evaluate_model(model, dataloader):
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in dataloader:
            inputs, labels = batch
            outputs = model(inputs)
            preds = torch.argmax(outputs, dim=1)

            all_preds.extend(preds.tolist())
            all_labels.extend(labels.tolist())

    accuracy = accuracy_score(all_labels, all_preds)
    precision = precision_score(all_labels, all_preds, average='weighted')
    recall = recall_score(all_labels, all_preds, average='weighted')
    f1 = f1_score(all_labels, all_preds, average='weighted')

    print(f"Evaluation Results:\n Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1 Score: {f1:.4f}")

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
    duofragment = StoryFragment(
        name="Duofragment",
        theme="balanced duality",
        archetype="The Harmonizer",
        elements=["maintaining equilibrium", "blending opposites"]
    )
    gentuo_fragment = StoryFragment(
        name="Gentuo",
        theme="innovative adaptability",
        archetype="The Visionary",
        elements=["transforming challenges into opportunities", "harnessing the power of creativity"]
    )
    return [lincoln_fragment, vajrayogini_fragment, vajrapani_fragment, duofragment, gentuo_fragment]

def train_model(base_model, custom_layer, quantum_layer, dataloader, num_epochs):
    model = ModifiedModel(base_model, custom_layer, quantum_layer)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=5)
    criterion = nn.CrossEntropyLoss()

    writer = SummaryWriter("./logs")

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for batch_idx, batch in enumerate(dataloader):
            try:
                inputs, labels = batch

                # Ensure inputs are FloatTensors and labels are LongTensors
                inputs = inputs.float()
                labels = labels.long()

                optimizer.zero_grad()

                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            except RuntimeError as e:
                print(f"Runtime error during training at epoch {epoch}, batch {batch_idx}: {e}")
                continue  # Skip this batch and continue training
            except Exception as e:
                print(f"Unexpected error at epoch {epoch}, batch {batch_idx}: {e}")
                continue

        avg_loss = total_loss / len(dataloader)
        writer.add_scalar("Loss", avg_loss, epoch)
        scheduler.step(avg_loss)

        print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {avg_loss:.4f}")

    writer.close()
    return model



if __name__ == "__main__":
    # Setup directories and tokenizer
    tokenizer_dir = "./OliviaAI"
    os.makedirs(tokenizer_dir, exist_ok=True)

    csv_path = "code_dataset.csv"  # Ensure this file exists with 'code' and 'label' columns
    tokenizer = setup_tokenizer_from_dataset(csv_path, tokenizer_dir)

    # Prepare dataset
    df = pd.read_csv(csv_path)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    max_length = 128
    train_dataset = CodeDataset(train_df, tokenizer, max_length)
    test_dataset = CodeDataset(test_df, tokenizer, max_length)

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=16)

    # Define a simple base model
    class BaseModel(nn.Module):
        def __init__(self, input_dim, hidden_dim, output_dim):
            super(BaseModel, self).__init__()
            self.fc1 = nn.Linear(input_dim, hidden_dim)
            self.activation = nn.ReLU()
            self.fc2 = nn.Linear(hidden_dim, output_dim)

        def forward(self, x):
            x = self.activation(self.fc1(x))
            return self.fc2(x)

    input_dim = max_length
    hidden_dim = 256
    output_dim = len(df['label'].unique())

    base_model = BaseModel(input_dim, hidden_dim, output_dim)
    custom_layer = CustomLayer(output_dim, 128)
    quantum_layer = QuantumLayer(128, 64)

    # Train the model
    trained_model = train_model(base_model, custom_layer, quantum_layer, train_loader, num_epochs=10)

    # Evaluate the model
    evaluate_model(trained_model, test_loader)

    # Generate a dynamic story
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
