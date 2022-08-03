from google.cloud import translate_v2 as translate


class Translator:
    def __init__(self, cred_json_file: str):
        self.client = translate.Client.from_service_account_json(cred_json_file)

    def translate(self, words: str) -> str:
        result = self.client.translate(words, target_language='tr')
        return result['translatedText']

