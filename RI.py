class ReplicaInteraction:
    def __init__(self, olivia_instance, replica_instance):
        self.olivia = olivia_instance
        self.replica = replica_instance

    def initiate_interaction(self):
        if self.replica.is_active:
            print("Interacting with the replica...")
            self.olivia.communicate_with_replica(self.replica)
            self.replica.respond_to_olivia(self.olivia)
        else:
            print("Replica is not active for interaction.")