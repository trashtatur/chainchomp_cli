from typing import List

import requests
from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel


class ChainlinkStartHandler:

    @staticmethod
    def contact_other_chainlinks(chainfile_model: ChainfileModel, urls_done: dict) -> dict:
        ChainlinkStartHandler.__contact_previous_links(chainfile_model.next_link, urls_done, chainfile_model.get_serialized(), 'next')
        ChainlinkStartHandler.__contact_previous_links(chainfile_model.previous_link, urls_done, chainfile_model.get_serialized(), 'previous')
        return urls_done

    @staticmethod
    def __contact_previous_links(
            list_of_links: List[str],
            urls_done: dict,
            serialized_model: dict,
            contact_type: str
    ):
        for url in list_of_links:
            if url not in urls_done['url_tries'].keys():
                urls_done['url_tries'][url] = 0
            if urls_done['url_tries'][url] >= 10 and url not in urls_done[contact_type]:
                urls_done[contact_type].append(url)
            if url in urls_done['urls_done']:
                continue
            url = f"http://{url.split('::')[0]}:{4410}"
            params = {'chainfile': serialized_model}
            response = requests.get(url=url, params=params, timeout=1)
            if response.status_code == 200:
                urls_done[contact_type].append(url)
            urls_done['url_tries'][url] += 1
