class OliviaAI:
    def __init__(self):
        self.astro_core = QuantumAstrophysicsCore(4)
        self.data_analyzer = AstrophysicalDataAnalyzer()
        self.trajectory_optimizer = QuantumTrajectoryOptimizer()
    
    def simulate_phenomena(self, phenomenon):
        if phenomenon == "hawking_radiation":
            return self.astro_core.simulate_hawking_radiation()
        elif phenomenon == "gravitational_waves":
            return self.astro_core.simulate_gravitational_waves()
        else:
            raise ValueError("Unknown phenomenon")

    def analyze_data(self, data_type, data):
        if data_type == "telescope":
            return self.data_analyzer.process_telescope_data(data)
        elif data_type == "gravitational_wave":
            return self.data_analyzer.analyze_gravitational_wave_signals(data)
        else:
            raise ValueError("Unknown data type")

    def optimize_mission(self, initial_conditions, constraints):
        return self.trajectory_optimizer.optimize_trajectory(initial_conditions, constraints)