import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


def send_email(
    to_email: str,
    subject: str,
    body: str,
    is_html: bool = False,
    cc_email: str = None,
    sender_name: str = None,
) -> bool:
    """
    Gmail SMTP를 통해 이메일을 발송합니다.

    Args:
        to_email:    수신자 이메일 주소
        subject:     이메일 제목
        body:        이메일 본문 (HTML 또는 plain text)
        is_html:     True이면 HTML 형식으로 발송 (기본: False)
        cc_email:    참조자 이메일 주소 (선택)
        sender_name: 발신자 표시 이름 (기본: 환경변수 MAIL_SENDER_NAME 또는 "System")

    Returns:
        발송 성공 여부 (bool)

    Required ENV:
        MAIL_USER     — Gmail 계정 주소
        MAIL_PASSWORD — Gmail 앱 비밀번호 (2단계 인증 필요)

    Optional ENV:
        MAIL_CC_DEFAULT  — 기본 참조자 이메일 (cc_email 미지정 시 사용)
        MAIL_SENDER_NAME — 발신자 표시 이름

    Example:
        from common_core.notifier import send_email
        send_email("user@example.com", "알림", "<h1>안녕하세요</h1>", is_html=True)
    """
    mail_user = os.getenv("MAIL_USER")
    mail_pass = os.getenv("MAIL_PASSWORD")

    if not mail_user or not mail_pass:
        logger.error("[EMAIL] 설정 누락: MAIL_USER 또는 MAIL_PASSWORD 환경변수를 확인하세요.")
        return False

    # 테스트 도메인 차단
    if "@example.com" in to_email:
        logger.warning(f"[EMAIL] 테스트용 주소 발송 차단: {to_email}")
        return True

    # 기본 참조자 적용 (환경변수)
    if not cc_email:
        cc_email = os.getenv("MAIL_CC_DEFAULT")

    display_name = sender_name or os.getenv("MAIL_SENDER_NAME", "System")

    try:
        msg = MIMEMultipart()
        msg["From"] = f"{display_name} <{mail_user}>"
        msg["To"] = to_email
        if cc_email:
            msg["Cc"] = cc_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html" if is_html else "plain", "utf-8"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(mail_user, mail_pass)
            server.send_message(msg)

        logger.info(f"[EMAIL] 발송 완료 → {to_email}")
        return True

    except Exception as e:
        logger.error(f"[EMAIL] 발송 실패 → {to_email}: {e}")
        return False
