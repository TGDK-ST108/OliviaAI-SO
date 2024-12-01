class Vertebrae:
    def __init__(self, id, content):
        self.id = id
        self.content = content  # Data contained in this vertebra
        self.next_vertebra = None  # Link to the next vertebra in sequence
    
    def set_next(self, next_vertebra):
        self.next_vertebra = next_vertebra
    
    def __repr__(self):
        return f"Vertebrae {self.id}: {self.content}"

class Expansionizer:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
    
    def add_vertebra(self, content):
        """Adds a new vertebra at the end."""
        new_vertebra = Vertebrae(self.length + 1, content)
        if self.head is None:
            self.head = new_vertebra
            self.tail = new_vertebra
        else:
            self.tail.set_next(new_vertebra)
            self.tail = new_vertebra
        self.length += 1
    
    def expand_vertebra(self, vertebra_id, new_content):
        """Expands the content of a specific vertebra based on its ID."""
        current = self.head
        while current:
            if current.id == vertebra_id:
                current.content += " | " + new_content
                print(f"Expanded Vertebrae {vertebra_id} with new content: '{new_content}'")
                return
            current = current.next_vertebra
        print(f"Vertebrae {vertebra_id} not found.")
    
    def traverse(self):
        """Traverses through the vertebrae in sequence."""
        current = self.head
        while current:
            print(current)
            current = current.next_vertebra

    def query_vertebra(self, vertebra_id):
        """Queries a specific vertebra by its ID."""
        current = self.head
        while current:
            if current.id == vertebra_id:
                return current
            current = current.next_vertebra
        return None


# Example usage
if __name__ == "__main__":
    expansionizer = Expansionizer()
    
    # Adding vertebrae (data segments)
    expansionizer.add_vertebra("Initial content of vertebra 1")
    expansionizer.add_vertebra("Initial content of vertebra 2")
    expansionizer.add_vertebra("Initial content of vertebra 3")

    # Expanding specific vertebrae with new data
    expansionizer.expand_vertebra(2, "Expanded data for vertebra 2")
    
    # Traversing the vertebrae to display contents
    print("\nTraversing the vertebrae data:")
    expansionizer.traverse()
    
    # Querying a specific vertebra
    vertebra_3 = expansionizer.query_vertebra(3)
    print(f"\nQuery result for vertebra 3: {vertebra_3}")