import json

import requests

from .job import Job
from .uniprot import UniProt


class NewJobError(Exception):
    pass


class VarQ():
    def __init__(self, protocol: str, host: str):
        self.protocol = protocol
        self.host = host
        self.api_url = f"{protocol}://{host}/api"

    def new_job(self, uniprot_id: str, pdb_id: str, sas=[]) -> Job:
        """ Starts or retrieves a job for a single PDB and list of SASs """
        url = f"{self.api_url}/new-job"
        payload = {"uniprotId": uniprot_id, "pdbIds": [pdb_id], "sas": sas}
        r = requests.post(url, json=payload).json()
        if r["error"]:
            raise NewJobError(r["error"])

        return Job(self.protocol, self.host, r["id"])

    def get_unp(self, uniprot_id: str) -> UniProt:
        """ Retrieve one UniProt entry by ID """
        url = f"{self.api_url}/uniprot/{uniprot_id}"
        return UniProt.from_json(requests.get(url).text)

    def is_online(self) -> bool:
        """ Returns the VarQ backend status """
        url = f"{self.api_url}/status"
        return requests.get(url).json()["status"] == "online"
