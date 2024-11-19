
from dataclasses import dataclass

@dataclass
class SequenceData:
    id: int
    name: str
    sequence: str
    description: str = ''
    sequence_type: str = 'DNA'  # Options: DNA, RNA, Protein
