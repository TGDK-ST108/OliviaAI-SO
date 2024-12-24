class UnifiedMedicalFramework:
    def __init__(self, olivia_ai):
        self.real_time_monitoring = RealTimeMonitoring(olivia_ai)
        self.veterinary_genomics = VeterinaryGenomics(olivia_ai)
        self.telemedicine = Telemedicine(olivia_ai)
        self.global_health_monitoring = GlobalHealthMonitoring(olivia_ai)

    def monitor_human_health(self, patient_id, real_time_data):
        return self.real_time_monitoring.monitor_human_patient(patient_id, real_time_data)

    def monitor_animal_health(self, animal_id, species, real_time_data):
        return self.real_time_monitoring.monitor_animal(animal_id, species, real_time_data)

    def analyze_genomics(self, species, gene_data):
        return self.veterinary_genomics.analyze_genomic_data(species, gene_data)

    def compare_genomics(self, human_genome, animal_genome):
        return self.veterinary_genomics.correlate_human_animal_genomics(human_genome, animal_genome)

    def consult_remotely(self, patient_type, patient_data):
        return self.telemedicine.remote_consultation(patient_type, patient_data)

    def monitor_global_health(self, human_data_stream, animal_data_stream):
        return self.global_health_monitoring.aggregate_health_data(human_data_stream, animal_data_stream)