import requests


class CoralClient:
    """Cliente HTTP para comunicação com Coral

    :param str coral_url: Endereço da API do serviço Coral
    """

    def __init__(self, coral_url, atlantis_client_id):
        self.coral_url = coral_url
        self.atlantis_client_id = atlantis_client_id


class CoralSyncClient(CoralClient):
    """Cliente HTTP para sincronização dos arquivos do banco de dados do Coral

    """

    def __init__(self, coral_url, atlantis_client_id, api_key):
        super().__init__(coral_url, atlantis_client_id)
        self.api_key = api_key

    def upsert_file(self, bucket, key, last_modified, size, metadata=None):
        """Crie ou atualiza um arquivo no banco do Coral.

        Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import TorpedoClient

            client = CoralClientSync('https://storage.spacetimeanalytics.com', 'atlantisclientid', 'apikey')
            response = client.upsert_file('spacetimelabs-bucket', '/folder/file.ext', '2020-06-26T14:51Z', 123, { 'thumb': 's3://bucket/folder/file.ext' })

        :param bucket: Bucket do arquivo
        :type bucket: str
        :param key: Chave do arquivo
        :type key: str
        :param last_modified: Data de última modificação do arquivo (Formato datetime ISO)
        :type last_modified: str
        :param size: Tamanho do arquivo em bytes
        :type size: int
        :param metadata: Dicionário de metadados do arquivo
        :type metadata: dict, optional
        :return: Resposta da requisição para o Coral
        :rtype: requests.Response
        """
        response = requests.post(
                '{}/api/sync'.format(self.coral_url),
                headers={
                    'bucket': bucket,
                    'atlantisclientid': self.atlantis_client_id,
                    'x-api-key': self.api_key
                }, params={
                    'key': key
                }, json={
                    'last_modified': last_modified,
                    'size': size,
                    'metadata': metadata,
                }
            )
        response.raise_for_status()
        return response

    def delete_file(self, bucket, key):
        """Remove um arquivo do banco do Coral.

        Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import TorpedoClient

            client = CoralClientSync('https://storage.spacetimeanalytics.com', 'atlantisclientid', 'apikey')
            response = client.delete_file('spacetimelabs-bucket', '/folder/file.ext')

        :param bucket: Bucket do arquivo
        :type bucket: str
        :param key: Chave do arquivo
        :type key: str
        :return: Resposta da requisição para o Coral
        :rtype: requests.Response
        """
        response = requests.delete(
                '{}/api/sync'.format(self.coral_url),
                headers={
                    'bucket': bucket,
                    'atlantisclientid': self.atlantis_client_id,
                    'x-api-key': self.api_key
                }, params={
                    'key': key
                }
            )
        response.raise_for_status()
        return response
