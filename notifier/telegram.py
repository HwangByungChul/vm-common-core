import os
import logging
import requests

logger = logging.getLogger(__name__)


def send_telegram_message(message: str, chat_id: str = None, parse_mode: str = "HTML") -> bool:
    """
    텔레그램 봇을 통해 메시지를 발송합니다.

    Args:
        message:    발송할 메시지 텍스트 (HTML 또는 Markdown 태그 허용)
        chat_id:    대상 채팅방 ID (미지정 시 환경변수 TELEGRAM_CHAT_ID 사용)
        parse_mode: 텍스트 파싱 방식 — "HTML" 또는 "Markdown" (기본: "HTML")

    Returns:
        발송 성공 여부 (bool)

    Required ENV:
        TELEGRAM_BOT_TOKEN — BotFather에서 발급받은 봇 토큰
        TELEGRAM_CHAT_ID   — 기본 수신 채팅방 ID

    Example:
        from common_core.notifier import send_telegram_message
        send_telegram_message("🚀 <b>배포 완료</b>\\n서버가 정상 실행 중입니다.")
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
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            logger.info(f"[TELEGRAM] 발송 완료 → chat_id: {target_chat_id}")
            return True
        else:
            logger.error(f"[TELEGRAM] 발송 실패: {response.status_code} — {response.text}")
            return False
    except Exception as e:
        logger.error(f"[TELEGRAM] 오류: {e}")
        return False
