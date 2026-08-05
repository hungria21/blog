import unittest
import os
import sqlite3
import config
import database
import downloader
import utils

class TestVideoDownloadBot(unittest.TestCase):

    def setUp(self):
        # Garante que as configurações padrão funcionam para os testes
        self.test_url = "https://www.w3schools.com/html/mov_bbb.mp4"
        self.temp_db = "test_cache.db"
        database.DB_FILE = self.temp_db
        database.init_db()

    def tearDown(self):
        # Remove DB de teste temporário
        if os.path.exists(self.temp_db):
            os.remove(self.temp_db)

    def test_config_validation(self):
        success, msg = config.validate_config()
        # No ambiente de testes, o API_ID pode estar como 123456 ou padrão, o que é válido sintaticamente
        self.assertIsInstance(success, bool)

    def test_database_operations(self):
        # Verifica se o cache vazio retorna None
        self.assertIsNone(database.get_cached_video(self.test_url))

        # Salva dados fictícios no cache
        database.save_cached_video(
            url=self.test_url,
            document_id=123456789,
            access_hash=987654321,
            file_reference=b"test_file_ref",
            mime_type="video/mp4",
            size=1024,
            title="Video de Teste",
            caption="Legenda rica formatada"
        )

        # Recupera dados
        cached = database.get_cached_video(self.test_url)
        self.assertIsNotNone(cached)
        self.assertEqual(cached["document_id"], 123456789)
        self.assertEqual(cached["access_hash"], 987654321)
        self.assertEqual(cached["file_reference"], b"test_file_ref")
        self.assertEqual(cached["mime_type"], "video/mp4")
        self.assertEqual(cached["size"], 1024)
        self.assertEqual(cached["title"], "Video de Teste")
        self.assertEqual(cached["caption"], "Legenda rica formatada")

    def test_utils_progress_bar(self):
        pbar = utils.generate_progress_bar(50)
        self.assertIn("██████████░░░░░░░░░░", pbar)
        self.assertIn("50.0%", pbar)

        # Extremos
        pbar_zero = utils.generate_progress_bar(-10)
        self.assertIn("0.0%", pbar_zero)
        pbar_hundred = utils.generate_progress_bar(150)
        self.assertIn("100.0%", pbar_hundred)

    def test_utils_format_size(self):
        self.assertEqual(utils.format_size(100), "100.00 B")
        self.assertEqual(utils.format_size(2048), "2.00 KB")
        self.assertEqual(utils.format_size(1048576 * 2.5), "2.50 MB")

    def test_utils_escape_html(self):
        text = "Hello <world> & 'friends'"
        escaped = utils.escape_html(text)
        self.assertEqual(escaped, "Hello &lt;world&gt; &amp; &#x27;friends&#x27;")

    def test_utils_format_rich_caption(self):
        title = "Super Vídeo do TikTok"
        desc = "Dança engraçada no pátio <legal>"
        author_username = "luiz_dançarino"
        author_name = "Luiz Dançarino"
        platform = "TikTok"
        url = "https://www.tiktok.com/@luiz_dancarino/video/112233"

        caption = utils.format_rich_caption(title, desc, author_username, author_name, platform, url)

        # Verificações de estrutura e escaping
        self.assertIn("<b>Super Vídeo do TikTok</b>", caption)
        self.assertIn("<i>Dança engraçada no pátio &lt;legal&gt;</i>", caption)
        self.assertIn('href="https://www.tiktok.com/@luiz_dançarino"', caption)
        self.assertIn("@luiz_dançarino", caption)
        self.assertIn("<b>Plataforma:</b> TikTok", caption)
        self.assertIn(f'href="{url}"', caption)

    def test_utils_platform_links(self):
        # Instagram
        caption_ig = utils.format_rich_caption("A", "B", "insta_user", "Insta", "Instagram", "http://ig")
        self.assertIn('href="https://www.instagram.com/insta_user/"', caption_ig)

        # Twitter / X
        caption_tw = utils.format_rich_caption("A", "B", "tw_user", "Tw", "Twitter / X", "http://tw")
        self.assertIn('href="https://x.com/tw_user"', caption_tw)

        # YouTube
        caption_yt = utils.format_rich_caption("A", "B", "yt_user", "Yt", "YouTube", "http://yt")
        self.assertIn('href="https://www.youtube.com/@yt_user"', caption_yt)

    def test_downloader_platform_name(self):
        self.assertEqual(downloader.get_platform_name("https://vm.tiktok.com/ZS12345/"), "TikTok")
        self.assertEqual(downloader.get_platform_name("https://www.instagram.com/p/C123/"), "Instagram")
        self.assertEqual(downloader.get_platform_name("https://twitter.com/user/status/123"), "Twitter / X")
        self.assertEqual(downloader.get_platform_name("https://x.com/user/status/123"), "Twitter / X")
        self.assertEqual(downloader.get_platform_name("https://www.youtube.com/watch?v=123"), "YouTube")
        self.assertEqual(downloader.get_platform_name("https://site.com/video.mp4"), "Rede Social")

if __name__ == "__main__":
    unittest.main()
