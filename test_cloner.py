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

        # Reseta as variáveis do módulo config para valores em branco/padrão
        self.original_api_id = config.API_ID
        self.original_api_hash = config.API_HASH
        self.original_source = config.SOURCE_CHANNEL
        self.original_dest = config.DESTINATION_CHANNEL

        config.API_ID = 0
        config.API_HASH = ""
        config.SOURCE_CHANNEL = ""
        config.DESTINATION_CHANNEL = ""

    def tearDown(self):
        if os.path.exists("progress.json"):
            os.remove("progress.json")

        # Restaura as variáveis de ambiente originais
        for key, val in self.env_patches.items():
            if val is not None:
                os.environ[key] = val
            elif key in os.environ:
                del os.environ[key]

        # Restaura as variáveis do módulo config
        config.API_ID = self.original_api_id
        config.API_HASH = self.original_api_hash
        config.SOURCE_CHANNEL = self.original_source
        config.DESTINATION_CHANNEL = self.original_dest

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

    def test_get_credentials_env(self):
        # Testa a leitura com variáveis de ambiente válidas
        os.environ["API_ID"] = "123456"
        os.environ["API_HASH"] = "abcdef"
        os.environ["SOURCE_CHANNEL"] = "@my_source"
        os.environ["DESTINATION_CHANNEL"] = "-100123456789"

        creds = config.get_credentials()
        self.assertEqual(creds["api_id"], 123456)
        self.assertEqual(creds["api_hash"], "abcdef")
        self.assertEqual(creds["source"], "@my_source")
        self.assertEqual(creds["destination"], -100123456789)

    def test_get_credentials_static(self):
        # Testa a leitura com variáveis estáticas configuradas no config.py
        config.API_ID = 987654
        config.API_HASH = "static_hash"
        config.SOURCE_CHANNEL = -100987654321
        config.DESTINATION_CHANNEL = "@dest_channel"

        creds = config.get_credentials()
        self.assertEqual(creds["api_id"], 987654)
        self.assertEqual(creds["api_hash"], "static_hash")
        self.assertEqual(creds["source"], -100987654321)
        self.assertEqual(creds["destination"], "@dest_channel")

    def test_get_credentials_missing_raises_exit(self):
        # Sem configuração, deve encerrar com SystemExit (sys.exit(1))
        with self.assertRaises(SystemExit):
            config.get_credentials()

if __name__ == "__main__":
    unittest.main()
