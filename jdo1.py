from tokenizers import ByteLevelBPETokenizer

# Initialize a tokenizer
tokenizer = ByteLevelBPETokenizer()

# Train the tokenizer on your dataset
tokenizer.train(files=["code_dataset.csv"], vocab_size=30000, min_frequency=2, special_tokens=[
    "<s>", "<pad>", "</s>", "<unk>", "<mask>",
])

# Save the tokenizer to a directory
tokenizer.save_model("OliviaAI")
