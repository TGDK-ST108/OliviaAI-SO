class RewardSystem:
    def __init__(self):
        self.rewards = []

    def grant_reward(self, task_completed, olivia_instance):
        if task_completed == "replica_sequencing":
            # Trigger visual feedback
            self.activate_visual_effects(olivia_instance)
            # Provide advanced features
            self.unlock_features(olivia_instance)
            # Update OliviaAI's experience database
            self.update_learning_module(olivia_instance)
            print("Reward granted for successful sequencing!")

    def activate_visual_effects(self, olivia_instance):
        # Enhance holographic orb
        olivia_instance.display_hologram("celebration_effect")
        olivia_instance.orb.glow_effect = True
        print("Celebratory visuals activated.")

    def unlock_features(self, olivia_instance):
        # Temporarily unlock advanced capabilities
        olivia_instance.enable_advanced_interactions = True
        print("Advanced features unlocked temporarily.")

    def update_learning_module(self, olivia_instance):
        # Improve her capabilities by integrating new learning modules
        olivia_instance.integrate_knowledge("Advanced Sequencing Techniques")
        print("Learning modules updated.")

# Example usage:
reward_system = RewardSystem()
task_completed = "replica_sequencing"
reward_system.grant_reward(task_completed, OliviaAI)