import logging
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

class CompoundFragmentAnalyzer:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def analyze_fragment(self, fragment_smiles):
        """Analyze a compound fragment given its SMILES representation."""
        try:
            # Create a molecule from the SMILES representation
            molecule = Chem.MolFromSmiles(fragment_smiles)
            if molecule is None:
                logging.error(f"Invalid SMILES: {fragment_smiles}")
                return None
            
            # Calculate molecular weight
            mol_weight = rdMolDescriptors.CalcExactMolWt(molecule)

            # Calculate number of atoms and fragments
            num_atoms = molecule.GetNumAtoms()
            num_bonds = molecule.GetNumBonds()

            # Get basic properties
            properties = {
                'SMILES': fragment_smiles,
                'Molecular Weight': mol_weight,
                'Number of Atoms': num_atoms,
                'Number of Bonds': num_bonds,
                'Formal Charge': Chem.rdMolDescriptors.CalcFormalCharge(molecule),
            }

            logging.info(f"Analyzed fragment: {properties}")
            return properties

        except Exception as e:
            logging.error(f"Error analyzing fragment {fragment_smiles}: {e}")
            return None

    def analyze_multiple_fragments(self, fragment_smiles_list):
        """Analyze multiple compound fragments."""
        results = {}
        for fragment in fragment_smiles_list:
            results[fragment] = self.analyze_fragment(fragment)
        return results

# Example usage:
if __name__ == "__main__":
    analyzer = CompoundFragmentAnalyzer()
    
    # List of compound fragments in SMILES format
    fragments = [
        "CCO",          # Ethanol
        "CC(=O)O",     # Acetic acid
        "C1=CC=CC=C1", # Benzene
        "C1CCC1"       # Cyclopropane
    ]

    # Analyze multiple fragments
    analysis_results = analyzer.analyze_multiple_fragments(fragments)
    
    for fragment, properties in analysis_results.items():
        print(f"Fragment: {fragment}, Properties: {properties}")
