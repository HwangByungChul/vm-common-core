# vm-common-core 사용 가이드 (Usage Guide)

`vm-common-core`는 여러 AI 에이전트 프로젝트에서 반복되는 핵심 로직을 통합하여 제공하는 공통 모듈 라이브러리입니다.

## 1. 프로젝트 설정 및 활용
상세한 모듈별 사용법은 `setup_guide.md`를 참고하세요.

## 2. AI 에이전트 개발을 위한 마스터 프롬프트 (Example)
이 프롬프트는 Antigravity와 같이 개발할 때 `vm-common-core`를 가장 효과적으로 활용하도록 지시하는 템플릿입니다.

---

### 로또 & 주식 추천 에이전트 개발 프롬프트

```markdown
# [Full-Stack AI 에이전트 개발] 로또 & 주식 추천 시스템 개발 요청

`vm-common-core` 라이브러리를 기반으로, 전문적인 데이터 분석을 통해 로또 번호와 주식 종목을 추천하는 **AI 에이전트 시스템**을 구축하세요.

## 1. 기반 인프라 및 환경 설정 (.env)
- **AI/LLM**: `OPENAI_API_KEY` 활용
- **Database**: `DATABASE_URL` 및 `VECTOR_DB_URL` 활용
- **Notification**: `TELEGRAM_BOT_TOKEN` 및 `TELEGRAM_CHAT_ID` 활용
- **Auth**: `JWT_SECRET_KEY` 및 `GOOGLE_CLIENT_ID` 활용

## 2. vm-common-core 모듈 통합 규칙
- **인증(Auth)**: `auth.guards.get_current_user`를 모든 추천 API에 적용.
- **데이터베이스(DB)**:
    - 모든 모델에 `TimestampMixin` 적용.
    - 추천 생성 시 `db.audit.AuditLog`에 활동 내역 기록.
- **알림(Notifier)**: `notifier.telegram.BaseTelegramBot` 클래스를 상속받아 봇 핸들러 구현.
- **AI 파이프라인**:
    - 리서치 파일 로드 시 `loaders.document_loader` 사용.
    - `VectorStoreFactory`를 통해 벡터 DB 인터페이스 구축.
    - `BaseAgentState`를 선언한 LangGraph 워크플로우로 구성.

## 3. 핵심 비즈니스 로직 요구사항
- **Lotto Node**: 과거 당첨 데이터 분석 및 가중치/Cold Number 알고리즘 적용.
- **Stock Node**: 시장 데이터(pykrx 등) 및 리서치 자료를 결합한 추천 엔진.
- **Service**: FastAPI 기반 REST API 및 텔레그램 `/lotto`, `/stock` 명령어 연동.
```

---

## 3. 주요 모듈별 코드 예시

### Notifier (Telegram)
```python
from common_core.notifier.telegram import BaseTelegramBot

class MyLottoBot(BaseTelegramBot):
    def handle_command(self, chat_id, text, username):
        if text == "/lotto":
            # 추천 로직 실행 후 메시지 발송
            self.send_telegram_message(f"행운의 번호: 1, 2, 3, 4, 5, 6", chat_id)
```

### DB (Audit Log)
```python
from common_core.db.audit import AuditLog
from common_core.db.database import SessionLocal

def log_action(user_id, action, details):
    db = SessionLocal()
    audit = AuditLog(user_id=user_id, action=action, details=details)
    db.add(audit)
    db.commit()
```
