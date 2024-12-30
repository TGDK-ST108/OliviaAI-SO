class HiggsFieldMapper:
    def __init__(self, quantum_sensors):
        self.quantum_sensors = quantum_sensors

    def map_field(self, environment_conditions):
        """
        Simulate Higgs field interactions under extraterrestrial conditions.
        """
        field_map = {}
        for condition in environment_conditions:
            field_map[condition] = self.quantum_sensors.capture(condition)
        return field_map

# Example Usage
quantum_sensors = QuantumSensors()
higgs_mapper = HiggsFieldMapper(quantum_sensors)
field_map = higgs_mapper.map_field(["low_gravity", "high_radiation"])
print("Higgs Field Map:", field_map)