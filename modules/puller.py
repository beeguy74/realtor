from typing import Optional
import requests


class Puller:
    url = "https://gateway.chotot.com/v1/public/ad-listing"
    params = {
        "cg": "1000",
        "page": "1",
        "sp": "1",
        "st": "u,h",
        "limit": "20",
        "fingerprint": "e4be10a5-efd6-4593-937c-7c82ff5f2d27",
        "include_expired_ads": "true",
        "key_param_included": "true"
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru,en-US;q=0.9,en;q=0.8",
        "ct-fingerprint": "e4be10a5-efd6-4593-937c-7c82ff5f2d27",
        "ct-platform": "web",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "referer": "https://www.nhatot.com/"
    }
    
    def __init__(self, url: Optional[str]=None, params: Optional[dict]=None, headers: Optional[dict]=None):
        """
        Initialize the Puller instance with optional URL, parameters, and headers.

        Args:
            url (Optional[str]): The URL to be used for requests. If provided, sets the instance's url attribute.
            params (Optional[dict]): Query parameters to be included in requests. If provided, sets the instance's params attribute.
            headers (Optional[dict]): HTTP headers to be included in requests. If provided, sets the instance's headers attribute.
        """
        if url:
            self.url = url
        if params:
            self.params = params
        if headers:
            self.headers = headers
            
    def __str__(self):
        return f"Puller class\nurl: {self.url}\nparams: {self.params}\n headers: {self.headers}"
        
    def make_request(self, output_file: Optional[str]):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(response.text)


if __name__ == "__main__":
    puller = Puller()
    print(puller)