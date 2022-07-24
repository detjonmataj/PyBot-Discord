import requests


class CompilerExplorerAPI:
    api_url = "https://compiler-explorer.com/api"

    @staticmethod
    def get_languages(*fields):

        if len(fields) == 0:
            fields = "all"
        else:
            fields = ",".join(fields)

        return requests.get(f"{CompilerExplorerAPI.api_url}/languages?fields={fields}", headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }).json()

    @staticmethod
    def get_compilers(*fields):
        if len(fields) == 0:
            fields = "all"
        else:
            fields = ",".join(fields)

        return requests.get(f"{CompilerExplorerAPI.api_url}/compilers?fields={fields}", headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }).json()
