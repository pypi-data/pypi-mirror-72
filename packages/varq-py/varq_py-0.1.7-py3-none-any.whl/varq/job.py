from dataclasses import dataclass, field
from typing import List, Optional

import requests
from dataclasses_json import LetterCase, config, dataclass_json

from .structure import Residue, StructureResults

STATUS = {
    0: "in queue",
    1: "processing",
    2: "done",
}


class PositionError(Exception):
    pass


class NotFoundInResults(Exception):
    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Request:
    name: str
    uniprot_id: str
    pdb_ids: List[str]
    sas: List[str]
    ip: str
    email: str
    time: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Results:
    id: str
    request: Request
    status: str
    started: str
    ended: str


class Job():
    def __init__(self, protocol: str, host: str, job_id: str):
        self.host = host
        self.protocol = protocol
        self.api_url = f"{protocol}://{host}/api"
        self.id = job_id
        self._update()

    def _update(self):
        url = f"{self.api_url}/job/{self.id}"
        self.overview = Results.from_json(requests.get(url).text)
        if self.overview.status == 2:
            struct_res_url = f"{url}/{self.overview.request.pdb_ids[0]}"
            self.results = StructureResults.from_json(requests.get(struct_res_url).text)
            self._create_mappings()

    @property
    def _unp_mappings(self):
        return self.results.pdb.sifts.uniprot[self.overview.request.uniprot_id].mappings

    @property
    def status(self):
        self._update()
        status_code = self.overview.status
        return status_code, STATUS[status_code]

    def _create_mappings(self):
        self.mappings = {}
        for chain in self._unp_mappings:
            self.mappings[chain.chain_id] = -chain.unp_start + chain.start.residue_number

    def _check_bounds(self, unp_pos: int):
        included = False
        for chain in self._unp_mappings:
            if chain.unp_start <= unp_pos <= chain.unp_end:
                included = True
                break
        if not included:
            raise PositionError("UniProt position not included in PDB structure.")

    def _has_residue(self, res_list: List[Residue], unp_pos: int) -> bool:
        self._check_bounds(unp_pos)
        for res in res_list:
            if res.position == self.unp_to_pdb(res.chain, unp_pos):
                return True
        return False

    def unp_to_pdb(self, chain: str, unp_pos: int) -> int:
        return self.mappings[chain] + unp_pos

    def ddg(self, sas: str) -> float:
        for f in self.results.stability.foldx:
            s = f.sas
            if s.from_aa + str(s.position) + s.to_aa == sas and f.in_structure:
                return f.dd_g
        raise NotFoundInResults("SAS not found in FoldX results.")

    def buried(self, unp_pos: int) -> bool:
        return self._has_residue(self.results.exposure.residues, unp_pos)

    def catalytic(self, unp_pos: int) -> bool:
        return self._has_residue(self.results.binding.catalytic.residues, unp_pos)

    def near_ligands(self, unp_pos: int) -> bool:
        near = []
        for lig, residues in self.results.binding.ligands.items():
            if self._has_residue(residues, unp_pos):
                near.append(lig)
        return near

    def interface(self, unp_pos: int) -> bool:
        return self._has_residue(self.results.interaction.residues, unp_pos)

    def pocket(self, unp_pos: int) -> bool:
        for pocket in self.results.binding.pockets:
            if self._has_residue(pocket.residues, unp_pos):
                return True
        return False
