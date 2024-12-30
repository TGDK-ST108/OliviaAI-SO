class MaterialOptimizer:
    def __init__(self, higgs_field_data):
        self.higgs_data = higgs_field_data

    def optimize_material(self, material_properties):
        """
        Optimize material properties based on Higgs field dynamics.
        """
        optimized_properties = {}
        for property, value in material_properties.items():
            optimized_properties[property] = value * self.higgs_data.get("field_intensity", 1.0)
        return optimized_properties

# Example Usage
higgs_data = {"field_intensity": 1.25}
optimizer = MaterialOptimizer(higgs_data)
optimized_material = optimizer.optimize_material({"density": 5000, "strength": 300})
print("Optimized Material Properties:", optimized_material)