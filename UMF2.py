class UnifiedMedicalFramework:
    def __init__(self, olivia_ai):
        self.clinical_integration = RealTimeClinicalIntegration(olivia_ai)
        self.veterinary_integration = VeterinaryMedicineIntegration(olivia_ai)

    def monitor_human_patient(self, patient_id, real_time_data):
        # Real-time clinical monitoring
        return self.clinical_integration.monitor_patient(patient_id, real_time_data)

    def analyze_animal_health(self, species, disease_data):
        # Veterinary health simulations
        return self.veterinary_integration.simulate_animal_health(species, disease_data)

    def correlate_human_animal_health(self, human_data, animal_data):
        # Cross-species disease analysis
        return self.veterinary_integration.analyze_cross_species_disease(human_data, animal_data)