import json

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

    @staticmethod
    def compile(source_code: str = None, language: str = None, compiler_id: str = None, compiler_options: str = "",
                args=None,
                stdin: str = ""):
        if source_code is None:
            raise ValueError("Code is required")
        if language is None and compiler_id is None:
            raise ValueError("Either language or compiler is required")

        if args is None:
            args = []

        data = {
            "source": source_code,
            "compiler": compiler_id,
            "options": {
                "userArguments": compiler_options,
                "executeParameters": {
                    "args": args,
                    "stdin": stdin
                },
                "compilerOptions": {
                    "executorRequest": True
                },
                "filters": {
                    "execute": True
                },
                "tools": [],
                "libraries": [
                    {"id": "openssl", "version": "111c"}
                ]
            },
            "lang": language,
            "allowStoreCodeDebug": True,
            "bypassCache": True
        }
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        try:
            return requests.post(f"{CompilerExplorerAPI.api_url}/compiler/{compiler_id}/compile", data=json.dumps(data),
                                 headers=headers)
        except Exception as e:
            raise "Error while communicating with the compiler-explorer API" from e
