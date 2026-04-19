import os
import logging
import requests

logger = logging.getLogger(__name__)


def send_telegram_message(message: str, chat_id: str = None, parse_mode: str = "HTML") -> bool:
    """
    텔레그램 봇을 통해 메시지를 발송합니다.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    target_chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    if not token or not target_chat_id:
        logger.warning("[TELEGRAM] 설정 누락: TELEGRAM_BOT_TOKEN 또는 TELEGRAM_CHAT_ID를 확인하세요.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": target_chat_id,
        "text": message,
        "parse_mode": parse_mode,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"[TELEGRAM] 오류: {e}")
        return False


def send_telegram_photo(photo_path: str, caption: str = None, chat_id: str = None) -> bool:
    """
    텔레그램 봇을 통해 이미지를 발송합니다.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    target_chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    if not token or not target_chat_id or not os.path.exists(photo_path):
        return False

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    try:
        with open(photo_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": target_chat_id, "caption": caption, "parse_mode": "HTML"}
            response = requests.post(url, data=data, files=files, timeout=20)
            return response.status_code == 200
    except Exception as e:
        logger.error(f"[TELEGRAM_PHOTO] 오류: {e}")
        return False


class BaseTelegramBot:
    """
    공통 텔레그램 봇 베이스 클래스.
    각 프로젝트에서 이를 상속받아 handle_command를 구현하여 사용합니다.
    """
    def __init__(self, token: str = None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def get_updates(self, offset=None):
        url = f"{self.base_url}/getUpdates"
        params = {"timeout": 20, "offset": offset}
        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
            return None

    def start_polling(self):
        logger.info("🤖 Telegram Bot Polling Started...")
        offset = None
        if not self.token:
            logger.error("❌ TELEGRAM_BOT_TOKEN이 설정되지 않았습니다.")
            return

        while True:
            try:
                updates = self.get_updates(offset)
                if updates and updates.get("ok"):
                    for update in updates.get("result", []):
                        offset = update["update_id"] + 1
                        self.process_update(update)
                import time
                time.sleep(1)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                import time
                time.sleep(5)

    def process_update(self, update):
        message = update.get("message")
        if message and "text" in message:
            chat_id = message["chat"]["id"]
            text = message["text"]
            username = message["from"].get("username", "Unknown")
            self.handle_command(chat_id, text, username)

    def handle_command(self, chat_id, text, username):
        """상속받는 클래스에서 구현 필요"""
        pass
