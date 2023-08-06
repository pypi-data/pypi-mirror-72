from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import LetterCase, config, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ClinVar:
    variation_id: int
    name: str
    clin_sig: str
    clin_sig_simple: int
    review_status: str
    phenotypes: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Variant:
    id: str
    position: int
    from_aa: str
    to_aa: str
    change: str
    note: str
    evidence: str
    dbsnp: str
    clinvar: Optional[ClinVar] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GlycoSite:
    position: int
    note: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Disulfide:
    positions: List[int]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PTMs:
    disulfide_bonds: Optional[List[Disulfide]] = None
    glycosilation_sites: Optional[List[GlycoSite]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UniProt:
    id: str
    url: str
    txt_url: str
    sequence: str
    name: str
    gene: str
    organism: str
    pdb_ids: Optional[List[str]] = None
    ptms: Optional[PTMs] = None
    variants: Optional[List[Variant]] = None
