from dataclasses import dataclass, field
from typing import Dict, List, Optional

import requests
from dataclasses_json import LetterCase, config, dataclass_json


def name(n):
    return field(default=None, metadata=config(field_name=n))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Residue:
    chain: str
    struct_position: int
    position: int
    name1: str


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class ResPos:
    residue_number: int


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class ChainMapping:
    start: ResPos
    end: ResPos
    chain_id: str
    struct_asym_id: str
    unp_start: int
    unp_end: int


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class SIFTSUniProt:
    identifier: str
    name: str
    mappings: List[ChainMapping]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SIFTS:
    uniprot: Optional[Dict[str, SIFTSUniProt]] = name("UniProt")


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PDB:
    id: str
    url: str
    pdb_url: str
    title: str
    date: str
    method: str
    resolution: float
    het_groups: List[str]
    sifts: SIFTS = field(metadata=config(field_name="SIFTS"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SAS:
    position: int
    from_aa: str
    to_aa: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FoldXSAS:
    sas: SAS
    in_structure: bool
    dd_g: float


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Stability:
    duration: int
    error: Optional[str] = None
    foldx: Optional[List[FoldXSAS]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Exposure:
    duration: int
    error: Optional[str] = None
    residues: Optional[List[Residue]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Pocket:
    name: str
    drug_score: float
    residues: Optional[List[Residue]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Catalytic:
    uniprot_positions: List[int]
    residues: Optional[List[Residue]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Binding:
    duration: int
    error: Optional[str] = None
    pockets: Optional[List[Pocket]] = None
    catalytic: Optional[Catalytic] = None
    ligands: Optional[Dict[str, List[Residue]]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Interaction:
    duration: int
    error: Optional[str] = None
    residues: Optional[List[Residue]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class StructureResults:
    pdb: PDB
    stability: Optional[Stability] = None
    exposure: Optional[Exposure] = None
    binding: Optional[Binding] = None
    interaction: Optional[Interaction] = None
