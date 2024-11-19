# dnadiatonic_analyzer.py

import logging
import re
from typing import List, Dict, Any

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DNADiatonicAnalyzer:
    def __init__(self):
        """
        Initialize the DNADiatonicAnalyzer.
        """
        logging.info("DNADiatonicAnalyzer initialized.")
    
    def collect_dna_data(self, source: str) -> str:
        """
        Collect DNA data from the specified source.

        :param source: Path to the DNA data file or an identifier for the data source.
        :return: DNA sequence as a string.
        """
        logging.info(f"Collecting DNA data from source: {source}")
        try:
            # Placeholder for different data source handling
            if source.endswith('.txt') or source.endswith('.fasta'):
                with open(source, 'r') as file:
                    dna_data = self._parse_fasta(file.read())
            else:
                # Implement other data source types as needed
                logging.error("Unsupported data source format.")
                dna_data = ""
            logging.info(f"DNA data collected successfully from {source}.")
            return dna_data
        except FileNotFoundError:
            logging.error(f"DNA data file not found: {source}")
            return ""
        except Exception as e:
            logging.error(f"Error collecting DNA data from {source}: {e}")
            return ""
    
    def _parse_fasta(self, fasta_content: str) -> str:
        """
        Parse FASTA formatted content to extract DNA sequence.

        :param fasta_content: Content of a FASTA file as a string.
        :return: DNA sequence as a string.
        """
        logging.info("Parsing FASTA formatted DNA data.")
        lines = fasta_content.strip().split('\n')
        sequence = ''.join(line.strip() for line in lines if not line.startswith('>'))
        logging.debug(f"Extracted DNA sequence: {sequence}")
        return sequence
    
    def process_data(self, dna_data: str) -> Dict[str, Any]:
        """
        Process and analyze the DNA data.

        :param dna_data: DNA sequence as a string.
        :return: Dictionary containing analysis results.
        """
        logging.info("Starting DNA data processing.")
        if not self.validate_dna_sequence(dna_data):
            logging.error("Invalid DNA sequence format.")
            return {"error": "Invalid DNA sequence format."}
        
        analysis_results = {}
        # Example analysis: Find specific motifs
        motifs = ["ATG", "TATA", "GGGCCC"]
        analysis_results['motifs_found'] = self.find_motifs(dna_data, motifs)
        
        # Example analysis: GC Content
        analysis_results['gc_content'] = self.calculate_gc_content(dna_data)
        
        # Add more analysis as needed
        
        logging.info("DNA data processing completed.")
        logging.debug(f"Analysis Results: {analysis_results}")
        return analysis_results
    
    def validate_dna_sequence(self, sequence: str) -> bool:
        """
        Validate the DNA sequence format.

        :param sequence: DNA sequence as a string.
        :return: True if valid, False otherwise.
        """
        logging.info("Validating DNA sequence format.")
        # Valid DNA sequence contains only A, T, G, C (case-insensitive)
        if re.fullmatch(r'[ATGCatgc]+', sequence):
            logging.info("DNA sequence is valid.")
            return True
        else:
            logging.warning("DNA sequence contains invalid characters.")
            return False
    
    def find_motifs(self, sequence: str, motifs: List[str]) -> Dict[str, int]:
        """
        Find and count specific motifs within the DNA sequence.

        :param sequence: DNA sequence as a string.
        :param motifs: List of motif strings to search for.
        :return: Dictionary with motif counts.
        """
        logging.info("Searching for motifs within DNA sequence.")
        motif_counts = {}
        for motif in motifs:
            count = len(re.findall(motif, sequence))
            motif_counts[motif] = count
            logging.debug(f"Motif '{motif}' found {count} times.")
        return motif_counts
    
    def calculate_gc_content(self, sequence: str) -> float:
        """
        Calculate the GC content percentage of the DNA sequence.

        :param sequence: DNA sequence as a string.
        :return: GC content as a float percentage.
        """
        logging.info("Calculating GC content of DNA sequence.")
        gc_count = sequence.count('G') + sequence.count('C') + sequence.count('g') + sequence.count('c')
        total = len(sequence)
        gc_content = (gc_count / total) * 100 if total > 0 else 0
        logging.info(f"GC Content: {gc_content:.2f}%")
        return gc_content
    
    def generate_report(self, analysis_results: Dict[str, Any], report_path: str):
        """
        Generate a report based on the analysis results.

        :param analysis_results: Dictionary containing analysis results.
        :param report_path: Path to save the generated report.
        """
        logging.info(f"Generating report at {report_path}")
        try:
            with open(report_path, 'w') as report_file:
                report_file.write("DNA Data Analysis Report\n")
                report_file.write("========================\n\n")
                
                if 'error' in analysis_results:
                    report_file.write(f"Error: {analysis_results['error']}\n")
                else:
                    report_file.write("Motifs Found:\n")
                    for motif, count in analysis_results.get('motifs_found', {}).items():
                        report_file.write(f"  {motif}: {count}\n")
                    
                    report_file.write(f"\nGC Content: {analysis_results.get('gc_content', 0):.2f}%\n")
                    
                    # Add more sections based on analysis_results
                    
            logging.info(f"Report generated successfully at {report_path}")
        except Exception as e:
            logging.error(f"Failed to generate report at {report_path}: {e}")
    
    # Example usage
    if __name__ == "__main__":
        analyzer = DNADiatonicAnalyzer()
        dna_source = 'sample_dna.fasta'  # Ensure this file exists with proper FASTA format
        dna_sequence = analyzer.collect_dna_data(dna_source)
        results = analyzer.process_data(dna_sequence)
        report_file = 'dna_analysis_report.txt'
        analyzer.generate_report(results, report_file)
