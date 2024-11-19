class VariableSequenceLibrary:
    def __init__(self):
        """Initialize the VariableSequenceLibrary."""
        self.sequences = {}

    def add_sequence(self, name, sequence):
        """
        Add a new variable sequence to the library.

        Args:
            name (str): The name of the sequence.
            sequence (list): The sequence of variables.
        """
        if name in self.sequences:
            raise ValueError(f"Sequence '{name}' already exists.")
        self.sequences[name] = sequence
        print(f"Sequence '{name}' added successfully.")

    def get_sequence(self, name):
        """
        Retrieve a sequence by name.

        Args:
            name (str): The name of the sequence.

        Returns:
            list: The sequence of variables.
        """
        if name not in self.sequences:
            raise ValueError(f"Sequence '{name}' not found.")
        return self.sequences[name]

    def transform_sequence(self, name, transform_func):
        """
        Transform a sequence using a given function.

        Args:
            name (str): The name of the sequence.
            transform_func (function): The transformation function to apply.

        Returns:
            list: The transformed sequence.
        """
        sequence = self.get_sequence(name)
        transformed_sequence = [transform_func(var) for var in sequence]
        print(f"Sequence '{name}' transformed successfully.")
        return transformed_sequence

    def remove_sequence(self, name):
        """
        Remove a sequence from the library.

        Args:
            name (str): The name of the sequence.
        """
        if name not in self.sequences:
            raise ValueError(f"Sequence '{name}' not found.")
        del self.sequences[name]
        print(f"Sequence '{name}' removed successfully.")

    def list_sequences(self):
        """List all sequences in the library."""
        print("Available Sequences:")
        for name in self.sequences:
            print(f"- {name}: {self.sequences[name]}")
