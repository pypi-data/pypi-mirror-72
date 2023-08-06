
from .source import SourceDataset


class DatasetDiscoveryService:
    service_url = 'https://dataset-discovery-service-whzo2dewrq-de.a.run.app'

    def __init__(self, client, project_id):
        self.client = client
        self.project_id = project_id

    def get_dataset(self, name):
        resp = self.client.make_request(DatasetDiscoveryService.service_url, {'name': name})
        metadata = resp.json()
        return SourceDataset(name, metadata=metadata, client=self.client)

    def list_datasets(self):
        resp = self.client.make_request(DatasetDiscoveryService.service_url)
        return resp.json()['datasets']

