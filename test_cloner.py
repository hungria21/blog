import os
import json
import unittest
from unittest.mock import patch
import config
import main

class TestChannelCloner(unittest.TestCase):
    def setUp(self):
        # Limpa o arquivo de progresso de teste
        if os.path.exists("progress.json"):
            os.remove("progress.json")

        # Reseta as variáveis de ambiente relevantes
        self.env_patches = {
            "API_ID": os.environ.get("API_ID"),
            "API_HASH": os.environ.get("API_HASH"),
            "SOURCE_CHANNEL": os.environ.get("SOURCE_CHANNEL"),
            "DESTINATION_CHANNEL": os.environ.get("DESTINATION_CHANNEL"),
        }
        for key in self.env_patches:
            if key in os.environ:
                del os.environ[key]

    def tearDown(self):
        if os.path.exists("progress.json"):
            os.remove("progress.json")

        # Restaura as variáveis de ambiente originais
        for key, val in self.env_patches.items():
            if val is not None:
                os.environ[key] = val
            elif key in os.environ:
                del os.environ[key]

    def test_load_progress_default(self):
        # Se não há arquivo, deve retornar 0
        self.assertEqual(main.load_progress(), 0)

    def test_save_and_load_progress(self):
        # Salva o progresso e lê de volta
        main.save_progress(42)
        self.assertEqual(main.load_progress(), 42)

    def test_load_progress_corrupted(self):
        # Escreve um arquivo corrompido
        with open("progress.json", "w") as f:
            f.write("{invalid json}")
        self.assertEqual(main.load_progress(), 0)

    @patch("builtins.input")
    def test_get_credentials_env(self, mock_input):
        # Testa a leitura com variáveis de ambiente válidas
        os.environ["API_ID"] = "123456"
        os.environ["API_HASH"] = "abcdef"
        os.environ["SOURCE_CHANNEL"] = "@my_source"
        os.environ["DESTINATION_CHANNEL"] = "-100123456789"

        # Recarrega o módulo ou as variáveis estáticas que dependem do import inicial
        config.API_ID = "123456"
        config.API_HASH = "abcdef"
        config.SOURCE_CHANNEL = "@my_source"
        config.DESTINATION_CHANNEL = "-100123456789"

        creds = config.get_credentials()
        self.assertEqual(creds["api_id"], 123456)
        self.assertEqual(creds["api_hash"], "abcdef")
        self.assertEqual(creds["source"], "@my_source")
        self.assertEqual(creds["destination"], -100123456789)
        mock_input.assert_not_called()

if __name__ == "__main__":
    unittest.main()
