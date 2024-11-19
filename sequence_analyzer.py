# sequence_analyzer.py

from Bio.Seq import Seq
from Bio.SeqUtils import GC
import logging

class SequenceAnalyzer:
    def __init__(self, sequence):
        self.sequence = Seq(sequence.upper())

    def get_gc_content(self):
        gc_content = gc_fraction(self.sequence) * 100
        logging.info(f"GC Content: {gc_content}%")
        return gc_content

    def transcribe(self):
        rna_sequence = self.sequence.transcribe()
        logging.info(f"RNA Sequence: {rna_sequence}")
        return rna_sequence

    def translate(self):
        protein_sequence = self.sequence.translate(to_stop=True)
        logging.info(f"Protein Sequence: {protein_sequence}")
        return protein_sequence

    def complement(self):
        complement_seq = self.sequence.complement()
        logging.info(f"Complement Sequence: {complement_seq}")
        return complement_seq

    def reverse_complement(self):
        rev_complement_seq = self.sequence.reverse_complement()
        logging.info(f"Reverse Complement Sequence: {rev_complement_seq}")
        return rev_complement_seq

    # Additional analysis methods can be added here
