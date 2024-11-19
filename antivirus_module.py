import numpy as np
import pandas as pd

class Nanoparticle:
    def __init__(self, formula, name, properties, derivative_offset):
        self.formula = formula
        self.name = name
        self.properties = properties
        self.derivative_offset = derivative_offset

    def __repr__(self):
        return f"{self.name} ({self.formula}): {self.properties}, Derivative Offset: {self.derivative_offset}"

class SequencingMeasure:
    def __init__(self, name, description, unit):
        self.name = name
        self.description = description
        self.unit = unit

    def __repr__(self):
        return f"{self.name}: {self.description} ({self.unit})"

class CurrogatedManifold:
    def __init__(self):
        self.sequences = []

    def add_sequence(self, sequence):
        self.sequences.append(sequence)

    def measure_formula_input_metrics(self, metric_type):
        return [self.calculate_metric(sequence, metric_type) for sequence in self.sequences]

    def calculate_metric(self, sequence, metric_type):
        if metric_type == "duometric":
            metric_value = self.duometric_transformation(sequence)
        elif metric_type == "trimetric":
            metric_value = self.trimetric_transformation(sequence)
        elif metric_type == "quadrometric":
            metric_value = self.quadrometric_transformation(sequence)
        else:
            raise ValueError("Unknown metric type")

        return {
            "sequence": sequence,
            "type": metric_type,
            "value": metric_value
        }

    def duometric_transformation(self, sequence):
        return np.mean([ord(char) for char in sequence])  # Example of using ASCII values

    def trimetric_transformation(self, sequence):
        return np.std([ord(char) for char in sequence])  # Example of using ASCII values

    def quadrometric_transformation(self, sequence):
        return np.sum([ord(char) ** 2 for char in sequence])  # Example of using ASCII values

    def lineate_data(self, data_array):
        # Assuming data_array is a numpy array with shape (n, m) where m includes fields of interest
        lineated_results = {
            "field_9": np.mean(data_array[:, 9]),
            "field_41": np.mean(data_array[:, 41]),
            "field_42": np.mean(data_array[:, 42]),
            "field_47": np.mean(data_array[:, 47])
        }
        return lineated_results

class MetricSympathizer:
    def __init__(self, currogated_manifold):
        self.currogated_manifold = currogated_manifold
        self.offsets = {}  # Store offsets for void protocols

    def set_void_protocol_offset(self, metric_type, offset_value):
        self.offsets[metric_type] = offset_value

    def combine_measures(self):
        combined_results = {}
        for metric_type in ["duometric", "trimetric", "quadrometric"]:
            measures = self.currogated_manifold.measure_formula_input_metrics(metric_type)
            combined_value = self.apply_void_protocol_offset(measures, metric_type)
            combined_results[metric_type] = combined_value
        return combined_results

    def apply_void_protocol_offset(self, measures, metric_type):
        offset = self.offsets.get(metric_type, 0)
        adjusted_measures = []
        for measure in measures:
            adjusted_value = measure["value"] + offset
            adjusted_measures.append({
                "sequence": measure["sequence"],
                "type": metric_type,
                "adjusted_value": adjusted_value
            })
        return adjusted_measures

class DataAnalysisTool:
    def __init__(self):
        self.data = []

    def add_data(self, data):
        self.data.append(data)

    def calculate_variation(self):
        # Example variation calculation for the added data
        if not self.data:
            return None
        return np.std(self.data)

    def sequence_data(self):
        # Example sequencing with predetermined measures
        return [self.duometric_lineation_processor(data) for data in self.data]

    def duometric_lineation_processor(self, data):
        return np.mean([ord(char) for char in data])  # Example of using ASCII values

class ForceGRAVToolkit:
    def __init__(self):
        self.nanoparticles = []
        self.index = {}
        self.sequencing_measures = []
        self.currogated_manifold = CurrogatedManifold()
        self.metric_sympathizer = MetricSympathizer(self.currogated_manifold)
        self.data_analysis_tool = DataAnalysisTool()

    def add_nanoparticle(self, formula, name, properties, derivative_offset):
        nanoparticle = Nanoparticle(formula, name, properties, derivative_offset)
        self.nanoparticles.append(nanoparticle)
        self.index[formula] = nanoparticle

    def get_nanoparticle(self, formula):
        return self.index.get(formula, None)

    def list_nanoparticles(self):
        return self.nanoparticles

    def add_sequencing_measure(self, name, description, unit):
        measure = SequencingMeasure(name, description, unit)
        self.sequencing_measures.append(measure)

    def list_sequencing_measures(self):
        return self.sequencing_measures

# Initialize the toolkit
force_grav_toolkit = ForceGRAVToolkit()

# List of nanoparticle formulas and their properties with derivative offsets
nanoparticle_data = [
    ("FePt", "Iron Platinum Nanoparticles", "Magnetic and catalysis", "dFePt/dx"),
    ("AgAu", "Silver Gold Nanoparticles", "Bimetallic properties", "dAgAu/dx"),
    ("CuAg", "Copper Silver Nanoparticles", "Antimicrobial properties", "dCuAg/dx"),
    ("AgInSe₂", "Silver Indium Selenide Nanoparticles", "Photovoltaic applications", "dAgInSe₂/dx"),
    ("C60", "Buckminsterfullerene Nanoparticles", "Electrical properties", "dC60/dx"),
    ("Fe₂O₃", "Iron(III) Oxide Nanoparticles", "Pigment and catalysis", "dFe₂O₃/dx"),
    ("CoNi", "Cobalt Nickel Nanoparticles", "Magnetic applications", "dCoNi/dx"),
    ("YVO₄", "Yttrium Vanadate Nanoparticles", "Phosphor applications", "dYVO₄/dx"),
    ("Gd₂O₃", "Gadolinium Oxide Nanoparticles", "Nuclear applications", "dGd₂O₃/dx"),
    ("SnS", "Tin Sulfide Nanoparticles", "Photovoltaic and optoelectronics", "dSnS/dx"),
    ("LiFePO₄", "Lithium Iron Phosphate Nanoparticles", "Battery applications", "dLiFePO₄/dx"),
    ("SiO₂", "Silica Nanoparticles", "Catalysis and drug delivery", "dSiO₂/dx"),
    ("CaTiO₃", "Calcium Titanate Nanoparticles", "Piezoelectric properties", "dCaTiO₃/dx"),
    ("C_3N_4", "Graphitic Carbon Nitride Nanoparticles", "Photocatalytic applications", "dC_3N_4/dx"),
    ("CuCo₂O₄", "Copper Cobalt Oxide Nanoparticles", "Catalysis", "dCuCo₂O₄/dx"),
    ("AlCu", "Aluminum Copper Nanoparticles", "Bimetallic properties", "dAlCu/dx"),
    ("NaY", "Sodium Yttrium Nanoparticles", "Optical properties", "dNaY/dx"),
    ("HfO₂", "Hafnium Dioxide Nanoparticles", "High-k dielectric applications", "dHfO₂/dx"),
    ("SrFeO₃", "Strontium Iron Oxide Nanoparticles", "Magnetic and electronic properties", "dSrFeO₃/dx"),
    ("TiAl", "Titanium Aluminum Nanoparticles", "Alloy applications", "dTiAl/dx"),
    ("ZnTiO₃", "Zinc Titanate Nanoparticles", "Dielectric properties", "dZnTiO₃/dx"),
    ("NiCo₂O₄", "Nickel Cobalt Oxide Nanoparticles", "Supercapacitor applications", "dNiCo₂O₄/dx"),
    ("AgTiO₃", "Silver Titanium Oxide Nanoparticles", "Antibacterial properties", "dAgTiO₃/dx"),
    ("Si₃B", "Silicon Boride Nanoparticles", "High temperature resistance", "dSi₃B/dx"),
    ("CuFeSe₂", "Copper Iron Selenide Nanoparticles", "Photovoltaic applications", "dCuFeSe₂/dx"),
    ("Mo₂C", "Molybdenum Carbide Nanoparticles", "Catalytic applications", "dMo₂C/dx"),
    ("V₂O₅", "Vanadium Pentoxide Nanoparticles", "Catalysis", "dV₂O₅/dx"),
    ("GaAs", "Gallium Arsenide Nanoparticles", "Semiconductor applications", "dGaAs/dx"),
    ("Al_2O_3", "Alumina Nanoparticles", "Catalysis and ceramics", "dAl_2O_3/dx"),
    ("FeO", "Iron(II) Oxide Nanoparticles", "Magnetic properties", "dFeO/dx"),
    ("PbO", "Lead Oxide Nanoparticles", "Electronics and optics", "dPbO/dx"),
    ("NiTi", "Nickel Titanium Nanoparticles", "Shape memory alloys", "dNiTi/dx"),
    ("BaFe₁₂O₁₈", "Barium Hexaferrite Nanoparticles", "Magnetic applications", "dBaFe₁₂O₁₈/dx"),
    ("CuO", "Copper(II) Oxide Nanoparticles", "Catalysis and antibacterial properties", "dCuO/dx"),
    ("ZrO₂", "Zirconium Dioxide Nanoparticles", "Dental and ceramics", "dZrO₂/dx"),
    ("LiNiMnCoO₄", "Lithium Nickel Manganese Cobalt Oxide Nanoparticles", "Battery technology", "dLiNiMnCoO₄/dx"),
    ("ZnFe₂O₄", "Zinc Ferrite Nanoparticles", "Magnetic properties", "dZnFe₂O₄/dx"),
    ("TiN", "Titanium Nitride Nanoparticles", "Coating and hardening", "dTiN/dx"),
    ("Co₃O₄", "Cobalt(II,III) Oxide Nanoparticles", "Catalysis", "dCo₃O₄/dx"),
    ("Li₃PO₄", "Lithium Phosphate Nanoparticles", "Solid electrolytes", "dLi₃PO₄/dx"),
    ("AlN", "Aluminum Nitride Nanoparticles", "High thermal conductivity", "dAlN/dx"),
    ("Bi₂Te₃", "Bismuth Telluride Nanoparticles", "Thermoelectric applications", "dBi₂Te₃/dx"),
    ("Ge", "Germanium Nanoparticles", "Semiconductor applications", "dGe/dx"),
    ("InP", "Indium Phosphide Nanoparticles", "Photovoltaic and electronic applications", "dInP/dx"),
    ("GaSb", "Gallium Antimonide Nanoparticles", "Semiconductor applications", "dGaSb/dx"),
    ("Y₂O₃", "Yttrium Oxide Nanoparticles", "Optoelectronic applications", "dY₂O₃/dx"),
    ("NdFeB", "Neodymium Iron Boron Nanoparticles", "Permanent magnets", "dNdFeB/dx"),
    ("ZrC", "Zirconium Carbide Nanoparticles", "High temperature applications", "dZrC/dx"),
    ("BiCuSeO", "Bismuth Copper Selenide Oxide Nanoparticles", "Thermoelectric materials", "dBiCuSeO/dx"),
    ("MgFe₂O₄", "Magnesium Ferrite Nanoparticles", "Magnetic applications", "dMgFe₂O₄/dx"),
    ("TiO₃", "Titanium Trioxide Nanoparticles", "Dielectric applications", "dTiO₃/dx"),
    ("ZrS", "Zirconium Sulfide Nanoparticles", "Optoelectronic properties", "dZrS/dx"),
    ("CoS", "Cobalt Sulfide Nanoparticles", "Catalytic properties", "dCoS/dx"),
    ("BaCuO₂", "Barium Copper Oxide Nanoparticles", "Superconductors", "dBaCuO₂/dx"),
    ("LiTiO₃", "Lithium Titanate Nanoparticles", "Battery applications", "dLiTiO₃/dx"),
    ("AgInS₂", "Silver Indium Sulfide Nanoparticles", "Photovoltaic applications", "dAgInS₂/dx"),
    ("GaP", "Gallium Phosphide Nanoparticles", "Optoelectronic applications", "dGaP/dx"),
    ("Bi₂S₃", "Bismuth Sulfide Nanoparticles", "Photovoltaic applications", "dBi₂S₃/dx"),
    ("Ti_3C_2", "Titanium Carbide MXene Nanoparticles", "Conductive applications", "dTi_3C_2/dx"),
    ("CuTiO₃", "Copper Titanium Oxide Nanoparticles", "Catalytic properties", "dCuTiO₃/dx"),
    ("CuSe", "Copper Selenide Nanoparticles", "Photovoltaic applications", "dCuSe/dx"),
    ("MgO", "Magnesium Oxide Nanoparticles", "Ceramics and electronics", "dMgO/dx"),
    ("HfN", "Hafnium Nitride Nanoparticles", "High-temperature applications", "dHfN/dx"),
    ("NiZr", "Nickel Zirconium Nanoparticles", "Coating applications", "dNiZr/dx"),
    ("MnO", "Manganese(II) Oxide Nanoparticles", "Catalytic properties", "dMnO/dx"),
    ("SnO₂", "Tin(IV) Oxide Nanoparticles", "Catalysis and sensors", "dSnO₂/dx"),
    ("ZnS", "Zinc Sulfide Nanoparticles", "Optoelectronic applications", "dZnS/dx"),
    ("NiMoO₄", "Nickel Molybdenum Oxide Nanoparticles", "Catalysis", "dNiMoO₄/dx"),
    ("TiC", "Titanium Carbide Nanoparticles", "Cutting tools", "dTiC/dx"),
    ("Al₂TiO₅", "Aluminum Titanate Nanoparticles", "Thermal stability", "dAl₂TiO₅/dx"),
    ("SnTe", "Tin Telluride Nanoparticles", "Thermoelectric applications", "dSnTe/dx"),
    ("In₂O₃", "Indium Oxide Nanoparticles", "Transparent conductive oxide", "dIn₂O₃/dx"),
    ("CrO₃", "Chromium Trioxide Nanoparticles", "Oxidizing agent", "dCrO₃/dx"),
    ("CoSe", "Cobalt Selenide Nanoparticles", "Photovoltaic applications", "dCoSe/dx"),
    ("MgC", "Magnesium Carbon Nanoparticles", "High temperature applications", "dMgC/dx"),
    ("MoS₂", "Molybdenum Disulfide Nanoparticles", "Electronics and optics", "dMoS₂/dx"),
    ("Yb₂O₃", "Ytterbium Oxide Nanoparticles", "Laser applications", "dYb₂O₃/dx"),
    ("InGaN", "Indium Gallium Nitride Nanoparticles", "Optoelectronics", "dInGaN/dx"),
    ("PbS", "Lead Sulfide Nanoparticles", "Photovoltaic applications", "dPbS/dx"),
    ("TiAlN", "Titanium Aluminum Nitride Nanoparticles", "Coating applications", "dTiAlN/dx"),
    ("Co₃Se₄", "Cobalt Selenide Nanoparticles", "Photovoltaic applications", "dCo₃Se₄/dx"),
    ("ZnO", "Zinc Oxide Nanoparticles", "Catalysis and electronics", "dZnO/dx"),
    ("NaCl", "Sodium Chloride Nanoparticles", "Drug delivery", "dNaCl/dx"),
    ("GaN", "Gallium Nitride Nanoparticles", "High-power electronics", "dGaN/dx"),
    ("FeNi", "Iron Nickel Nanoparticles", "Magnetic applications", "dFeNi/dx"),
    ("AlFeO₃", "Aluminum Iron Oxide Nanoparticles", "Catalysis", "dAlFeO₃/dx"),
    ("CuBiS₂", "Copper Bismuth Sulfide Nanoparticles", "Photovoltaic applications", "dCuBiS₂/dx"),
    ("TiFe", "Titanium Iron Nanoparticles", "Metallic alloys", "dTiFe/dx"),
    ("CrN", "Chromium Nitride Nanoparticles", "Coating applications", "dCrN/dx"),
    ("AgPd", "Silver Palladium Nanoparticles", "Catalytic properties", "dAgPd/dx"),
    ("CoTiO₃", "Cobalt Titanium Oxide Nanoparticles", "Catalytic applications", "dCoTiO₃/dx"),
    ("Ga₂O₃", "Gallium Oxide Nanoparticles", "High temperature applications", "dGa₂O₃/dx"),
    ("BiFeO₃", "Bismuth Ferrite Nanoparticles", "Multiferroic properties", "dBiFeO₃/dx"),
    ("TiNi", "Titanium Nickel Nanoparticles", "Shape memory alloys", "dTiNi/dx"),
    ("In₂S₃", "Indium Sulfide Nanoparticles", "Photovoltaic applications", "dIn₂S₃/dx"),
    ("KTiOPO₄", "Potassium Titanyl Phosphate Nanoparticles", "Optical applications", "dKTiOPO₄/dx"),
    ("ZnAl₂O₄", "Zinc Aluminum Oxide Nanoparticles", "Catalytic properties", "dZnAl₂O₄/dx"),
    ("MgTiO₃", "Magnesium Titanate Nanoparticles", "Dielectric applications", "dMgTiO₃/dx"),
    ("AgCl", "Silver Chloride Nanoparticles", "Antibacterial properties", "dAgCl/dx"),
    ("AgBiS₂", "Silver Bismuth Sulfide Nanoparticles", "Photovoltaic applications", "dAgBiS₂/dx"),
    ("TiO₂", "Titanium Dioxide Nanoparticles", "Photocatalytic applications", "dTiO₂/dx"),
    ("FeCo", "Iron Cobalt Nanoparticles", "Magnetic properties", "dFeCo/dx"),
    ("MgCoO₃", "Magnesium Cobalt Oxide Nanoparticles", "Catalytic applications", "dMgCoO₃/dx"),
    ("BaPbO₃", "Barium Lead Oxide Nanoparticles", "Superconducting properties", "dBaPbO₃/dx"),
    ("ZnSe", "Zinc Selenide Nanoparticles", "Optoelectronic applications", "dZnSe/dx"),
    ("TiRu", "Titanium Ruthenium Nanoparticles", "Catalytic applications", "dTiRu/dx"),
    ("Bi₂O₃", "Bismuth Oxide Nanoparticles", "Optoelectronic applications", "dBi₂O₃/dx"),
    ("LiNiO₂", "Lithium Nickel Oxide Nanoparticles", "Battery applications", "dLiNiO₂/dx"),
    ("SnS₂", "Tin Disulfide Nanoparticles", "Optoelectronic applications", "dSnS₂/dx"),
    ("NiAl", "Nickel Aluminum Nanoparticles", "Alloy applications", "dNiAl/dx"),
    ("FeS", "Iron(II) Sulfide Nanoparticles", "Photovoltaic applications", "dFeS/dx"),
    ("MnTiO₃", "Manganese Titanate Nanoparticles", "Magnetic applications", "dMnTiO₃/dx"),
    ("CdS", "Cadmium Sulfide Nanoparticles", "Photovoltaic applications", "dCdS/dx"),
    ("AgZr", "Silver Zirconium Nanoparticles", "Bimetallic properties", "dAgZr/dx"),
    ("FeZnO₃", "Iron Zinc Oxide Nanoparticles", "Catalytic applications", "dFeZnO₃/dx"),
    ("TiO₄", "Titanium Tetroxide Nanoparticles", "Catalytic applications", "dTiO₄/dx"),
    ("TiRh", "Titanium Rhodium Nanoparticles", "Catalytic properties", "dTiRh/dx"),
    ("MgZrO₃", "Magnesium Zirconium Oxide Nanoparticles", "High-temperature applications", "dMgZrO₃/dx"),
    ("NiWO₄", "Nickel Tungsten Oxide Nanoparticles", "Catalytic applications", "dNiWO₄/dx"),
    ("ZnC", "Zinc Carbide Nanoparticles", "High temperature applications", "dZnC/dx"),
    ("CuSe₂", "Copper Diselenide Nanoparticles", "Photovoltaic applications", "dCuSe₂/dx"),
    ("AgGaO₂", "Silver Gallium Oxide Nanoparticles", "Optoelectronic applications", "dAgGaO₂/dx"),
    ("AgGaS₂", "Silver Gallium Sulfide Nanoparticles", "Photovoltaic applications", "dAgGaS₂/dx"),
    ("YFeO₃", "Yttrium Iron Oxide Nanoparticles", "Magnetic properties", "dYFeO₃/dx"),
    ("TiCoO₃", "Titanium Cobalt Oxide Nanoparticles", "Catalytic applications", "dTiCoO₃/dx"),
    ("CoAl₂O₄", "Cobalt Aluminum Oxide Nanoparticles", "Catalytic applications", "dCoAl₂O₄/dx"),
    ("FeTiO₃", "Iron Titanium Oxide Nanoparticles", "Magnetic properties", "dFeTiO₃/dx"),
    ("CuBi₂O₆", "Copper Bismuth Oxide Nanoparticles", "Catalytic applications", "dCuBi₂O₆/dx"),
    ("ZnMoO₄", "Zinc Molybdenum Oxide Nanoparticles", "Catalytic applications", "dZnMoO₄/dx"),
    ("TiSi₂", "Titanium Disilicide Nanoparticles", "Semiconductor applications", "dTiSi₂/dx"),
    ("NiCeO₃", "Nickel Cerium Oxide Nanoparticles", "Catalytic applications", "dNiCeO₃/dx"),
    ("FeCoCr", "Iron Cobalt Chromium Nanoparticles", "Alloy applications", "dFeCoCr/dx"),
    ("LiCoO₂", "Lithium Cobalt Oxide Nanoparticles", "Battery applications", "dLiCoO₂/dx"),
    ("AgCdTe", "Silver Cadmium Telluride Nanoparticles", "Photovoltaic applications", "dAgCdTe/dx"),
    ("TiMoO₄", "Titanium Molybdenum Oxide Nanoparticles", "Catalytic applications", "dTiMoO₄/dx"),
    ("ZnNiO₄", "Zinc Nickel Oxide Nanoparticles", "Catalytic applications", "dZnNiO₄/dx"),
    ("PbTiO₃", "Lead Titanate Nanoparticles", "Piezoelectric applications", "dPbTiO₃/dx"),
    ("CuTe", "Copper Telluride Nanoparticles", "Photovoltaic applications", "dCuTe/dx"),
    ("FeO", "Iron(II) Oxide Nanoparticles", "Magnetic properties", "dFeO/dx"),
    ("TiIn", "Titanium Indium Nanoparticles", "Alloy applications", "dTiIn/dx"),
    ("CuMoS₂", "Copper Molybdenum Disulfide Nanoparticles", "Photovoltaic applications", "dCuMoS₂/dx"),
    ("TiV", "Titanium Vanadium Nanoparticles", "Alloy applications", "dTiV/dx"),
    ("BiCuO₁", "Bismuth Copper Oxide Nanoparticles", "Superconducting properties", "dBiCuO₁/dx"),
    ("CuSn", "Copper Tin Nanoparticles", "Soldering applications", "dCuSn/dx"),
    ("FeO₃", "Iron(III) Oxide Nanoparticles", "Catalytic properties", "dFeO₃/dx"),
    ("InSe", "Indium Selenide Nanoparticles", "Photovoltaic applications", "dInSe/dx"),
    ("CoBi", "Cobalt Bismuth Nanoparticles", "Magnetic applications", "dCoBi/dx"),
    ("CuS", "Copper(II) Sulfide Nanoparticles", "Photovoltaic applications", "dCuS/dx"),
    ("CoCrO₄", "Cobalt Chromium Oxide Nanoparticles", "Catalytic applications", "dCoCrO₄/dx"),
    ("FeZnO", "Iron Zinc Oxide Nanoparticles", "Catalytic applications", "dFeZnO/dx"),
    ("CoS₂", "Cobalt Disulfide Nanoparticles", "Photovoltaic applications", "dCoS₂/dx"),
    ("CoO", "Cobalt(II) Oxide Nanoparticles", "Catalytic applications", "dCoO/dx"),
    ("CoMnO₄", "Cobalt Manganese Oxide Nanoparticles", "Catalytic applications", "dCoMnO₄/dx"),
    ("CuZnAl", "Copper Zinc Aluminum Nanoparticles", "Alloy applications", "dCuZnAl/dx"),
    ("FeBiO₃", "Iron Bismuth Oxide Nanoparticles", "Magnetic properties", "dFeBiO₃/dx"),
    ("FeMnO₄", "Iron Manganese Oxide Nanoparticles", "Catalytic applications", "dFeMnO₄/dx"),
    ("AgZnO", "Silver Zinc Oxide Nanoparticles", "Antibacterial properties", "dAgZnO/dx"),
    ("AlNiO₃", "Aluminum Nickel Oxide Nanoparticles", "Catalytic applications", "dAlNiO₃/dx"),
    ("CuMgO", "Copper Magnesium Oxide Nanoparticles", "Catalytic applications", "dCuMgO/dx"),
    ("CuSbS₂", "Copper Antimony Sulfide Nanoparticles", "Photovoltaic applications", "dCuSbS₂/dx"),
    ("AlTiO₃", "Aluminum Titanate Nanoparticles", "Thermal stability", "dAlTiO₃/dx"),
    ("SnSe", "Tin Selenide Nanoparticles", "Thermoelectric applications", "dSnSe/dx"),
    ("FeS₂", "Iron Disulfide Nanoparticles", "Photovoltaic applications", "dFeS₂/dx"),
    ("CuMoO₄", "Copper Molybdenum Oxide Nanoparticles", "Catalytic applications", "dCuMoO₄/dx"),
    ("AgBiO₃", "Silver Bismuth Oxide Nanoparticles", "Photovoltaic applications", "dAgBiO₃/dx"),
    ("MgZnO", "Magnesium Zinc Oxide Nanoparticles", "Optoelectronic applications", "dMgZnO/dx"),
    ("LiTiO₃", "Lithium Titanate Nanoparticles", "Battery applications", "dLiTiO₃/dx"),
    ("NiCrO₄", "Nickel Chromium Oxide Nanoparticles", "Catalytic applications", "dNiCrO₄/dx"),
    ("TiO₂-SiO₂", "Titanium Dioxide-Silica Nanoparticles", "Composite materials", "dTiO₂-SiO₂/dx"),
    ("InGaP", "Indium Gallium Phosphide Nanoparticles", "Optoelectronic applications", "dInGaP/dx"),
    ("YBa₂Cu₃O₇", "Yttrium Barium Copper Oxide Nanoparticles", "Superconducting properties", "dYBa₂Cu₃O₇/dx"),
    ("CuAg", "Copper Silver Nanoparticles", "Antibacterial properties", "dCuAg/dx"),
    ("ZnAlO₃", "Zinc Aluminum Oxide Nanoparticles", "Catalytic applications", "dZnAlO₃/dx"),
    ("CuSnS₂", "Copper Tin Sulfide Nanoparticles", "Photovoltaic applications", "dCuSnS₂/dx"),
    ("TiCrO₃", "Titanium Chromium Oxide Nanoparticles", "Catalytic applications", "dTiCrO₃/dx"),
    ("LiMnO₂", "Lithium Manganese Oxide Nanoparticles", "Battery applications", "dLiMnO₂/dx"),
    ("ZnGa₂O₄", "Zinc Gallium Oxide Nanoparticles", "Optoelectronic applications", "dZnGa₂O₄/dx"),
    ("CuCdS", "Copper Cadmium Sulfide Nanoparticles", "Photovoltaic applications", "dCuCdS/dx"),
    ("ZnO-ZnS", "Zinc Oxide-Zinc Sulfide Nanoparticles", "Composite materials", "dZnO-ZnS/dx"),
    ("AgCuO", "Silver Copper Oxide Nanoparticles", "Antibacterial properties", "dAgCuO/dx"),
    ("CuFeO₂", "Copper Iron Oxide Nanoparticles", "Catalytic applications", "dCuFeO₂/dx"),
    ("TiCr", "Titanium Chromium Nanoparticles", "Alloy applications", "dTiCr/dx"),
    ("NiCoO₂", "Nickel Cobalt Oxide Nanoparticles", "Catalytic applications", "dNiCoO₂/dx"),
    ("CuCoO₂", "Copper Cobalt Oxide Nanoparticles", "Catalytic applications", "dCuCoO₂/dx"),
    ("AgCuS", "Silver Copper Sulfide Nanoparticles", "Photovoltaic applications", "dAgCuS/dx"),
    ("CoO₃", "Cobalt(III) Oxide Nanoparticles", "Catalytic applications", "dCoO₃/dx"),
    ("AgPbS₂", "Silver Lead Sulfide Nanoparticles", "Photovoltaic applications", "dAgPbS₂/dx"),
    ("MgTiO₃-ZnO", "Magnesium Titanate-Zinc Oxide Nanoparticles", "Composite materials", "dMgTiO₃-ZnO/dx"),
    ("MgCoO", "Magnesium Cobalt Oxide Nanoparticles", "Catalytic applications", "dMgCoO/dx"),
    ("AgNi", "Silver Nickel Nanoparticles", "Catalytic applications", "dAgNi/dx"),
    ("CuCo₂S₃", "Copper Cobalt Sulfide Nanoparticles", "Photovoltaic applications", "dCuCo₂S₃/dx"),
    ("AgTiO₂", "Silver Titanium Dioxide Nanoparticles", "Antibacterial properties", "dAgTiO₂/dx"),
    ("ZnFe₂O₄", "Zinc Ferrite Nanoparticles", "Magnetic properties", "dZnFe₂O₄/dx"),
    ("FeS₃", "Iron Trisulfide Nanoparticles", "Photovoltaic applications", "dFeS₃/dx"),
    ("FeCoNi", "Iron Cobalt Nickel Nanoparticles", "Magnetic properties", "dFeCoNi/dx"),
    ("CoFe₂O₄", "Cobalt Ferrite Nanoparticles", "Magnetic properties", "dCoFe₂O₄/dx"),
    ("ZnFeO₃", "Zinc Iron Oxide Nanoparticles", "Catalytic applications", "dZnFeO₃/dx"),
    ("AgInTe₂", "Silver Indium Telluride Nanoparticles", "Photovoltaic applications", "dAgInTe₂/dx"),
    ("AgCuInSe₂", "Silver Copper Indium Selenide Nanoparticles", "Photovoltaic applications", "dAgCuInSe₂/dx"),
    ("TiC-TiN", "Titanium Carbide-Titanium Nitride Nanoparticles", "Composite materials", "dTiC-TiN/dx"),
    ("CuCdTe", "Copper Cadmium Telluride Nanoparticles", "Photovoltaic applications", "dCuCdTe/dx"),
    ("FeSiO₄", "Iron Silicate Nanoparticles", "Catalytic applications", "dFeSiO₄/dx"),
    ("AgAu", "Silver Gold Nanoparticles", "Catalytic properties", "dAgAu/dx"),
    ("TiAlO₃", "Titanium Aluminum Oxide Nanoparticles", "Thermal stability", "dTiAlO₃/dx"),
    ("FeMoO₄", "Iron Molybdenum Oxide Nanoparticles", "Catalytic applications", "dFeMoO₄/dx"),
    ("NiZrO₃", "Nickel Zirconium Oxide Nanoparticles", "Catalytic applications", "dNiZrO₃/dx"),
    ("FeCuS₂", "Iron Copper Sulfide Nanoparticles", "Photovoltaic applications", "dFeCuS₂/dx"),
    ("CuCoNi", "Copper Cobalt Nickel Nanoparticles", "Alloy applications", "dCuCoNi/dx"),
    ("SnCu", "Tin Copper Nanoparticles", "Soldering applications", "dSnCu/dx"),
    ("NiPb", "Nickel Lead Nanoparticles", "Alloy applications", "dNiPb/dx"),
    ("AgZnS", "Silver Zinc Sulfide Nanoparticles", "Photovoltaic applications", "dAgZnS/dx"),
    ("CoV₂O₅", "Cobalt Vanadium Oxide Nanoparticles", "Catalytic applications", "dCoV₂O₅/dx"),
    ("NiW", "Nickel Tungsten Nanoparticles", "Alloy applications", "dNiW/dx"),
    ("CoCuO", "Cobalt Copper Oxide Nanoparticles", "Catalytic applications", "dCoCuO/dx"),
    ("InP", "Indium Phosphide Nanoparticles", "Optoelectronic applications", "dInP/dx"),
    ("FeTe", "Iron Telluride Nanoparticles", "Photovoltaic applications", "dFeTe/dx"),
    ("FeBi", "Iron Bismuth Nanoparticles", "Magnetic applications", "dFeBi/dx"),
    ("NiAl₂O₄", "Nickel Aluminum Oxide Nanoparticles", "Catalytic applications", "dNiAl₂O₄/dx"),
    ("CuMgAl", "Copper Magnesium Aluminum Nanoparticles", "Alloy applications", "dCuMgAl/dx"),
    ("CoV", "Cobalt Vanadium Nanoparticles", "Magnetic applications", "dCoV/dx"),
    ("ZnS-ZnO", "Zinc Sulfide-Zinc Oxide Nanoparticles", "Composite materials", "dZnS-ZnO/dx"),
    ("ZnTiO₃", "Zinc Titanium Oxide Nanoparticles", "Catalytic applications", "dZnTiO₃/dx"),
    ("CuZnO", "Copper Zinc Oxide Nanoparticles", "Catalytic applications", "dCuZnO/dx"),
    ("ZnAg", "Zinc Silver Nanoparticles", "Catalytic properties", "dZnAg/dx"),
    ("MgFe₂O₄", "Magnesium Ferrite Nanoparticles", "Magnetic properties", "dMgFe₂O₄/dx"),
    ("AgSbS₂", "Silver Antimony Sulfide Nanoparticles", "Photovoltaic applications", "dAgSbS₂/dx"),
    ("FeRh", "Iron Rhodium Nanoparticles", "Magnetic applications", "dFeRh/dx"),
    ("NiZnO", "Nickel Zinc Oxide Nanoparticles", "Catalytic applications", "dNiZnO/dx"),
    ("ZnCoO", "Zinc Cobalt Oxide Nanoparticles", "Catalytic applications", "dZnCoO/dx"),
    ("AgPdAu", "Silver Palladium Gold Nanoparticles", "Catalytic properties", "dAgPdAu/dx"),
    ("AgSnS₂", "Silver Tin Sulfide Nanoparticles", "Photovoltaic applications", "dAgSnS₂/dx"),
    ("AgNiO₂", "Silver Nickel Oxide Nanoparticles", "Antibacterial properties", "dAgNiO₂/dx"),
    ("ZnCeO₃", "Zinc Cerium Oxide Nanoparticles", "Catalytic applications", "dZnCeO₃/dx"),
    ("CoCuZn", "Cobalt Copper Zinc Nanoparticles", "Alloy applications", "dCoCuZn/dx"),
    ("MgIn₂O₄", "Magnesium Indium Oxide Nanoparticles", "Catalytic applications", "dMgIn₂O₄/dx"),
    ("FeCoCu", "Iron Cobalt Copper Nanoparticles", "Alloy applications", "dFeCoCu/dx"),
    ("CuNiO₂", "Copper Nickel Oxide Nanoparticles", "Catalytic applications", "dCuNiO₂/dx"),
    ("CuAu", "Copper Gold Nanoparticles", "Catalytic properties", "dCuAu/dx"),
    ("CoCuNiFe", "Cobalt Copper Nickel Iron Nanoparticles", "Alloy applications", "dCoCuNiFe/dx"),
    ("ZnMnO", "Zinc Manganese Oxide Nanoparticles", "Catalytic applications", "dZnMnO/dx"),
    ("AgZnO-ZnS", "Silver Zinc Oxide-Zinc Sulfide Nanoparticles", "Composite materials", "dAgZnO-ZnS/dx"),
    ("CoMn", "Cobalt Manganese Nanoparticles", "Magnetic applications", "dCoMn/dx"),
    ("FeNiZn", "Iron Nickel Zinc Nanoparticles", "Alloy applications", "dFeNiZn/dx"),
    ("CuSnZn", "Copper Tin Zinc Nanoparticles", "Alloy applications", "dCuSnZn/dx"),
    ("FeCrO₄", "Iron Chromium Oxide Nanoparticles", "Catalytic applications", "dFeCrO₄/dx"),
    ("NiZr", "Nickel Zirconium Nanoparticles", "Alloy applications", "dNiZr/dx"),
    ("AgCuNi", "Silver Copper Nickel Nanoparticles", "Catalytic properties", "dAgCuNi/dx"),
    ("ZnTiFeO₄", "Zinc Titanium Iron Oxide Nanoparticles", "Catalytic applications", "dZnTiFeO₄/dx"),
    ("ZnFeO", "Zinc Iron Nanoparticles", "Catalytic applications", "dZnFeO/dx"),
    ("CoZrO₄", "Cobalt Zirconium Oxide Nanoparticles", "Catalytic applications", "dCoZrO₄/dx"),
    ("CuMo", "Copper Molybdenum Nanoparticles", "Alloy applications", "dCuMo/dx"),
    ("FeTiZr", "Iron Titanium Zirconium Nanoparticles", "Alloy applications", "dFeTiZr/dx"),
    ("ZnNiFeO₄", "Zinc Nickel Iron Oxide Nanoparticles", "Catalytic applications", "dZnNiFeO₄/dx"),
    ("MgCoNi", "Magnesium Cobalt Nickel Nanoparticles", "Alloy applications", "dMgCoNi/dx"),
    ("FeCoNiZr", "Iron Cobalt Nickel Zirconium Nanoparticles", "Alloy applications", "dFeCoNiZr/dx"),
    ("CuAgZn", "Copper Silver Zinc Nanoparticles", "Alloy applications", "dCuAgZn/dx"),
    ("ZnNiCo", "Zinc Nickel Cobalt Nanoparticles", "Alloy applications", "dZnNiCo/dx"),
    ("CuNiCo", "Copper Nickel Cobalt Nanoparticles", "Alloy applications", "dCuNiCo/dx"),
    ("FeCuNi", "Iron Copper Nickel Nanoparticles", "Alloy applications", "dFeCuNi/dx"),
    ("ZnNiCu", "Zinc Nickel Copper Nanoparticles", "Alloy applications", "dZnNiCu/dx"),
    ("NiCoFe", "Nickel Cobalt Iron Nanoparticles", "Alloy applications", "dNiCoFe/dx"),
    ("NiCuZn", "Nickel Copper Zinc Nanoparticles", "Alloy applications", "dNiCuZn/dx"),
    ("AgCuCo", "Silver Copper Cobalt Nanoparticles", "Alloy applications", "dAgCuCo/dx"),
    ("CoCuFe", "Cobalt Copper Iron Nanoparticles", "Alloy applications", "dCoCuFe/dx"),
    ("FeNiCu", "Iron Nickel Copper Nanoparticles", "Alloy applications", "dFeNiCu/dx"),
    ("ZnNiFe", "Zinc Nickel Iron Nanoparticles", "Alloy applications", "dZnNiFe/dx"),
    ("CoNiCu", "Cobalt Nickel Copper Nanoparticles", "Alloy applications", "dCoNiCu/dx"),
    ("ZnCoFe", "Zinc Cobalt Iron Nanoparticles", "Alloy applications", "dZnCoFe/dx"),
    ("NiZnFe", "Nickel Zinc Iron Nanoparticles", "Alloy applications", "dNiZnFe/dx"),
    ("CuNiFe", "Copper Nickel Iron Nanoparticles", "Alloy applications", "dCuNiFe/dx"),
    ("AgZnCu", "Silver Zinc Copper Nanoparticles", "Alloy applications", "dAgZnCu/dx"),
    ("CoZnFe", "Cobalt Zinc Iron Nanoparticles", "Alloy applications", "dCoZnFe/dx"),
    ("AgCoNi", "Silver Cobalt Nickel Nanoparticles", "Alloy applications", "dAgCoNi/dx"),
    ("FeZnCu", "Iron Zinc Copper Nanoparticles", "Alloy applications", "dFeZnCu/dx"),
    ("CoFeCu", "Cobalt Iron Copper Nanoparticles", "Alloy applications", "dCoFeCu/dx"),
    ("AgFeCu", "Silver Iron Copper Nanoparticles", "Alloy applications", "dAgFeCu/dx"),
    ("CuZnNi", "Copper Zinc Nickel Nanoparticles", "Alloy applications", "dCuZnNi/dx"),
    ("ZnCuFe", "Zinc Copper Iron Nanoparticles", "Alloy applications", "dZnCuFe/dx"),
    ("AgCuZnNi", "Silver Copper Zinc Nickel Nanoparticles", "Alloy applications", "dAgCuZnNi/dx"),
    ("ZnFeCu", "Zinc Iron Copper Nanoparticles", "Alloy applications", "dZnFeCu/dx"),
    ("CoCuZnNi", "Cobalt Copper Zinc Nickel Nanoparticles", "Alloy applications", "dCoCuZnNi/dx"),
    ("CuZnCoNi", "Copper Zinc Cobalt Nickel Nanoparticles", "Alloy applications", "dCuZnCoNi/dx"),
    ("NiZnCoFe", "Nickel Zinc Cobalt Iron Nanoparticles", "Alloy applications", "dNiZnCoFe/dx"),
    ("AgZnCoFe", "Silver Zinc Cobalt Iron Nanoparticles", "Alloy applications", "dAgZnCoFe/dx"),
    ("CoNiCuFe", "Cobalt Nickel Copper Iron Nanoparticles", "Alloy applications", "dCoNiCuFe/dx"),
    ("CuZnNiFe", "Copper Zinc Nickel Iron Nanoparticles", "Alloy applications", "dCuZnNiFe/dx"),
    ("NiFeCu", "Nickel Iron Copper Nanoparticles", "Alloy applications", "dNiFeCu/dx"),
    ("AgNiZn", "Silver Nickel Zinc Nanoparticles", "Alloy applications", "dAgNiZn/dx"),
    ("ZnCuNiFe", "Zinc Copper Nickel Iron Nanoparticles", "Alloy applications", "dZnCuNiFe/dx"),
    ("NiZnCuFe", "Nickel Zinc Copper Iron Nanoparticles", "Alloy applications", "dNiZnCuFe/dx"),
    ("ZnFeNi", "Zinc Iron Nickel Nanoparticles", "Alloy applications", "dZnFeNi/dx"),
    ("CoCuNiFe", "Cobalt Copper Nickel Iron Nanoparticles", "Alloy applications", "dCoCuNiFe/dx"),
    ("FeNiCo", "Iron Nickel Cobalt Nanoparticles", "Alloy applications", "dFeNiCo/dx"),
    ("CuZnFeNi", "Copper Zinc Iron Nickel Nanoparticles", "Alloy applications", "dCuZnFeNi/dx"),
    ("AgCuNiFe", "Silver Copper Nickel Iron Nanoparticles", "Alloy applications", "dAgCuNiFe/dx"),
    ("FeCuZnNi", "Iron Copper Zinc Nickel Nanoparticles", "Alloy applications", "dFeCuZnNi/dx"),
    ("NiCuFeCo", "Nickel Copper Iron Cobalt Nanoparticles", "Alloy applications", "dNiCuFeCo/dx"),
    ("AgCoCuFe", "Silver Cobalt Copper Iron Nanoparticles", "Alloy applications", "dAgCoCuFe/dx"),
    ("ZnFeCuNi", "Zinc Iron Copper Nickel Nanoparticles", "Alloy applications", "dZnFeCuNi/dx"),
    ("NiZnFeCo", "Nickel Zinc Iron Cobalt Nanoparticles", "Alloy applications", "dNiZnFeCo/dx"),
    ("CuNiZnFe", "Copper Nickel Zinc Iron Nanoparticles", "Alloy applications", "dCuNiZnFe/dx"),
    ("AgZnCuFe", "Silver Zinc Copper Iron Nanoparticles", "Alloy applications", "dAgZnCuFe/dx"),
    ("CoCuZnFe", "Cobalt Copper Zinc Iron Nanoparticles", "Alloy applications", "dCoCuZnFe/dx"),
    ("FeCoZn", "Iron Cobalt Zinc Nanoparticles", "Alloy applications", "dFeCoZn/dx"),
    ("ZnCuCoFe", "Zinc Copper Cobalt Iron Nanoparticles", "Alloy applications", "dZnCuCoFe/dx"),
    ("AgNiCo", "Silver Nickel Cobalt Nanoparticles", "Alloy applications", "dAgNiCo/dx"),
    ("ZnNiCoFe", "Zinc Nickel Cobalt Iron Nanoparticles", "Alloy applications", "dZnNiCoFe/dx"),
    ("FeNiZnCo", "Iron Nickel Zinc Cobalt Nanoparticles", "Alloy applications", "dFeNiZnCo/dx"),
    ("CuZnFeCo", "Copper Zinc Iron Cobalt Nanoparticles", "Alloy applications", "dCuZnFeCo/dx"),
    ("AgFeNi", "Silver Iron Nickel Nanoparticles", "Alloy applications", "dAgFeNi/dx"),
    ("CuFeZnCo", "Copper Iron Zinc Cobalt Nanoparticles", "Alloy applications", "dCuFeZnCo/dx"),
    ("FeZnCoNi", "Iron Zinc Cobalt Nickel Nanoparticles", "Alloy applications", "dFeZnCoNi/dx"),
    ("ZnCuFeCo", "Zinc Copper Iron Cobalt Nanoparticles", "Alloy applications", "dZnCuFeCo/dx"),
    ("AgCuZnCo", "Silver Copper Zinc Cobalt Nanoparticles", "Alloy applications", "dAgCuZnCo/dx"),
    ("NiZnCuCo", "Nickel Zinc Copper Cobalt Nanoparticles", "Alloy applications", "dNiZnCuCo/dx"),
    ("FeNiCuZn", "Iron Nickel Copper Zinc Nanoparticles", "Alloy applications", "dFeNiCuZn/dx"),
    ("CuNiCoZn", "Copper Nickel Cobalt Zinc Nanoparticles", "Alloy applications", "dCuNiCoZn/dx"),
    ("ZnFeCoNi", "Zinc Iron Cobalt Nickel Nanoparticles", "Alloy applications", "dZnFeCoNi/dx"),
    ("AgCoNiFe", "Silver Cobalt Nickel Iron Nanoparticles", "Alloy applications", "dAgCoNiFe/dx"),
    ("ZnNiCuCo", "Zinc Nickel Copper Cobalt Nanoparticles", "Alloy applications", "dZnNiCuCo/dx"),
    ("CoCuNiZn", "Cobalt Copper Nickel Zinc Nanoparticles", "Alloy applications", "dCoCuNiZn/dx"),
    ("FeCuZnCo", "Iron Copper Zinc Cobalt Nanoparticles", "Alloy applications", "dFeCuZnCo/dx"),
    ("CuZnFeNiCo", "Copper Zinc Iron Nickel Cobalt Nanoparticles", "Alloy applications", "dCuZnFeNiCo/dx"),
    ("FeCoZnNi", "Iron Cobalt Zinc Nickel Nanoparticles", "Alloy applications", "dFeCoZnNi/dx"),
    ("AgZnCuCo", "Silver Zinc Copper Cobalt Nanoparticles", "Alloy applications", "dAgZnCuCo/dx"),
    ("NiFeZnCo", "Nickel Iron Zinc Cobalt Nanoparticles", "Alloy applications", "dNiFeZnCo/dx"),
    ("AgNiFe", "Silver Nickel Iron Nanoparticles", "Alloy applications", "dAgNiFe/dx"),
    ("ZnCuCoZn", "Zinc Copper Cobalt Zinc Nanoparticles", "Alloy applications", "dZnCuCoZn/dx"),
    ("CoZnNiFe", "Cobalt Zinc Nickel Iron Nanoparticles", "Alloy applications", "dCoZnNiFe/dx"),
    ("FeCuCoNi", "Iron Copper Cobalt Nickel Nanoparticles", "Alloy applications", "dFeCuCoNi/dx"),
    ("AgFeZn", "Silver Iron Zinc Nanoparticles", "Alloy applications", "dAgFeZn/dx"),
    ("ZnCuNiZn", "Zinc Copper Nickel Zinc Nanoparticles", "Alloy applications", "dZnCuNiZn/dx"),
    ("CuFeNiZn", "Copper Iron Nickel Zinc Nanoparticles", "Alloy applications", "dCuFeNiZn/dx"),
    ("ZnNiFeCo", "Zinc Nickel Iron Cobalt Nanoparticles", "Alloy applications", "dZnNiFeCo/dx"),
    ("NiCoFeZn", "Nickel Cobalt Iron Zinc Nanoparticles", "Alloy applications", "dNiCoFeZn/dx"),
    ("AgCuZnZn", "Silver Copper Zinc Zinc Nanoparticles", "Alloy applications", "dAgCuZnZn/dx"),
    ("FeZnNiCu", "Iron Zinc Nickel Copper Nanoparticles", "Alloy applications", "dFeZnNiCu/dx"),
    ("ZnCuZnCo", "Zinc Copper Zinc Cobalt Nanoparticles", "Alloy applications", "dZnCuZnCo/dx"),
    ("CoFeZnNi", "Cobalt Iron Zinc Nickel Nanoparticles", "Alloy applications", "dCoFeZnNi/dx"),
    ("CuNiZnZn", "Copper Nickel Zinc Zinc Nanoparticles", "Alloy applications", "dCuNiZnZn/dx"),
    ("NiFeCuZn", "Nickel Iron Copper Zinc Nanoparticles", "Alloy applications", "dNiFeCuZn/dx"),
    ("AgNiZnZn", "Silver Nickel Zinc Zinc Nanoparticles", "Alloy applications", "dAgNiZnZn/dx"),
    ("ZnZnZn", "Zinc Zinc Zinc Nanoparticles", "Alloy applications", "dZnZnZn/dx"),
    ("FeFeZn", "Iron Iron Zinc Nanoparticles", "Alloy applications", "dFeFeZn/dx"),
    ("CoCoZn", "Cobalt Cobalt Zinc Nanoparticles", "Alloy applications", "dCoCoZn/dx"),
    ("AgAgZn", "Silver Silver Zinc Nanoparticles", "Alloy applications", "dAgAgZn/dx"),
    ("CuCuZn", "Copper Copper Zinc Nanoparticles", "Alloy applications", "dCuCuZn/dx"),
    ("NiNiZn", "Nickel Nickel Zinc Nanoparticles", "Alloy applications", "dNiNiZn/dx"),
    ("FeFeFe", "Iron Iron Iron Nanoparticles", "Alloy applications", "dFeFeFe/dx"),
    ("CoCoCo", "Cobalt Cobalt Cobalt Nanoparticles", "Alloy applications", "dCoCoCo/dx"),
]

# Add the nanoparticles to the toolkit
for formula, name, properties, derivative_offset in nanoparticle_data:
    force_grav_toolkit.add_nanoparticle(formula, name, properties, derivative_offset)

# Adding some sequencing measures
force_grav_toolkit.add_sequencing_measure("DNA Sequencing", "Determining the order of nucleotides in DNA", "Base pairs")
force_grav_toolkit.add_sequencing_measure("RNA Sequencing", "Analyzing the transcriptome", "Base pairs")
force_grav_toolkit.add_sequencing_measure("Protein Sequencing", "Determining amino acid sequences", "Amino acids")

# Example of measuring sequential structures and applying metrics
force_grav_toolkit.currogated_manifold.add_sequence("DNA Sequence 1")
force_grav_toolkit.currogated_manifold.add_sequence("RNA Sequence 1")
force_grav_toolkit.currogated_manifold.add_sequence("Protein Structure 1")

# Setting offsets for void protocols
force_grav_toolkit.metric_sympathizer.set_void_protocol_offset("duometric", 1.5)
force_grav_toolkit.metric_sympathizer.set_void_protocol_offset("trimetric", -0.5)
force_grav_toolkit.metric_sympathizer.set_void_protocol_offset("quadrometric", 2.0)

# Combining measures
combined_metrics = force_grav_toolkit.metric_sympathizer.combine_measures()

print("\nCombined Measures with Void Protocol Offsets:")
for metric_type, results in combined_metrics.items():
    print(f"\n{metric_type.capitalize()}:")
    for result in results:
        print(result)

# Example of lineating data in arrays
data_array = np.random.rand(100, 50)  # Random data for demonstration
lineated_results = force_grav_toolkit.currogated_manifold.lineate_data(data_array)

print("\nLineated Data Results:")
for field, value in lineated_results.items():
    print(f"{field}: {value}")

# Example of using the DataAnalysisTool
force_grav_toolkit.data_analysis_tool.add_data("Some data string 1")
force_grav_toolkit.data_analysis_tool.add_data("Another data string 2")

variation = force_grav_toolkit.data_analysis_tool.calculate_variation()
print(f"\nVariation of the data: {variation}")

sequenced_data = force_grav_toolkit.data_analysis_tool.sequence_data()
print("\nSequenced Data:")
print(sequenced_data)
