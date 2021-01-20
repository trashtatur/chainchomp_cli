import json
from typing import List

import requests
from chainchomplib import LoggerInterface
from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel


class ChainlinkStartHandler:

    PORT = 4410
    STRING_FOR_PREVIOUS = 'previous'
    STRING_FOR_NEXT = 'next'

    @staticmethod
    def contact_remote_chainlinks(chainfile_model: ChainfileModel, urls_done: dict) -> dict:
        ChainlinkStartHandler.__contact_remote_links(
            chainfile_model.next_links,
            urls_done,
            chainfile_model.get_serialized(),
            ChainlinkStartHandler.STRING_FOR_NEXT
        )
        ChainlinkStartHandler.__contact_remote_links(
            chainfile_model.previous_links,
            urls_done,
            chainfile_model.get_serialized(),
            ChainlinkStartHandler.STRING_FOR_PREVIOUS
        )
        return urls_done

    @staticmethod
    def contact_local_adapter(chainfile_model: ChainfileModel):
        url = f"http://localhost:{ChainlinkStartHandler.PORT}/chainfile/local/receive"
        params = {'chainfile': chainfile_model.get_serialized()}
        try:
            response = requests.post(url=url, data=json.dumps(params), timeout=1)
        except Exception:
            return False
        if response.status_code == 200:
            return True

        if response.status_code == 403 or response.status_code == 500:
            LoggerInterface.error(f'Error during transmission: {response.reason}')

        return False

    @staticmethod
    def __contact_remote_links(
            list_of_links: List[str],
            urls_done: dict,
            serialized_model: dict,
            contact_type: str
    ):
        for link_and_url in list_of_links:
            if link_and_url not in urls_done['url_tries'].keys():
                urls_done['url_tries'][link_and_url] = 0
            if urls_done['url_tries'][link_and_url] >= 10 and link_and_url not in urls_done[contact_type]:
                urls_done[contact_type].append(link_and_url)
            if link_and_url in urls_done[contact_type]:
                continue
            request_url = f"http://{link_and_url.split('::')[0]}:{ChainlinkStartHandler.PORT}/chainfile/remote/receive"
            params = {
                'chainfile': serialized_model,
                'is_next': contact_type == ChainlinkStartHandler.STRING_FOR_NEXT,
                'is_previous': contact_type == ChainlinkStartHandler.STRING_FOR_PREVIOUS,
                'name_of_called_link': link_and_url.split('::')[1]
            }
            try:
                response = requests.post(url=request_url, data=json.dumps(params), timeout=1)
            except requests.exceptions.ConnectTimeout:
                urls_done['url_tries'][link_and_url] += 1
                continue

            if response.status_code == 200:
                urls_done[contact_type].append(link_and_url)

            if response.status_code == 403 or response.status_code == 500:
                LoggerInterface.error(f'Error during transmission: {response.reason}')

            urls_done['url_tries'][link_and_url] += 1
