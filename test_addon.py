import sys
import os

# Mock xbmc and xbmcaddon
class MockAddon:
    def getAddonInfo(self, key):
        if key == 'path': return '.'
        if key == 'profile': return './profile'
        return ''
    def getSetting(self, key):
        return ''

sys.modules['xbmc'] = __import__('unittest.mock').Mock()
sys.modules['xbmcaddon'] = __import__('unittest.mock').Mock()
sys.modules['xbmcaddon'].Addon.return_value = MockAddon()

def test_imports():
    try:
        sys.path.append('plugin.service.telegramstream/resources/lib')
        from telethon import TelegramClient
        import pyaes
        import rsa
        print("Imports successful")
    except ImportError as e:
        print(f"Import failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_imports()
