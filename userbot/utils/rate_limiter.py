# coding: utf-8
import time
import asyncio
from telethon.errors import FloodWaitError
from userbot import logger

class RateLimiter:
    """
    Classe para controlar a taxa de requisições e evitar o banimento.
    Implementa um sistema de tokens para limitar ações por minuto e hora.
    """
    def __init__(self, requests_per_minute=20, requests_per_hour=100):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.minute_actions = []
        self.hour_actions = []

    def _cleanup_actions(self):
        """Remove ações antigas que já não contam para o limite."""
        current_time = time.time()
        self.minute_actions = [t for t in self.minute_actions if t > current_time - 60]
        self.hour_actions = [t for t in self.hour_actions if t > current_time - 3600]

    def can_execute(self):
        """Verifica se uma nova ação pode ser executada."""
        self._cleanup_actions()
        if len(self.minute_actions) >= self.requests_per_minute:
            return False
        if len(self.hour_actions) >= self.requests_per_hour:
            return False
        return True

    def add_action(self):
        """Registra uma nova ação."""
        current_time = time.time()
        self.minute_actions.append(current_time)
        self.hour_actions.append(current_time)

    async def wait_if_needed(self):
        """Aguarda se o limite de taxa for atingido."""
        while not self.can_execute():
            logger.warning("Limite de taxa atingido. Aguardando 10 segundos...")
            await asyncio.sleep(10)

    async def handle_flood_wait(self, error: FloodWaitError):
        """Gerencia um FloodWaitError aguardando o tempo necessário."""
        wait_time = error.seconds + 5  # Adiciona uma margem de segurança
        logger.warning(f"Recebido FloodWaitError. Aguardando {wait_time} segundos.")
        await asyncio.sleep(wait_time)

# Instância global do RateLimiter
rate_limiter = RateLimiter()
