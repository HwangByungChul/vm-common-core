# vm-common-core

> **VectorMoon 공통 핵심 패키지** — FastAPI 기반 풀스택 프로젝트의 반복 개발을 제거하고, 신규 프로젝트를 빠르게 시작하기 위한 공통 모듈 모음입니다.

---

## 📦 포함 모듈 개요

| 모듈 | 경로 | 기능 요약 |
|---|---|---|
| **인증** | `auth/` | JWT 발급/검증, Google OAuth 2.0, 권한 가드 |
| **알림** | `notifier/` | Gmail SMTP 이메일, 텔레그램 Bot 메시지 발송 |
| **데이터베이스** | `db/` | SQLAlchemy 엔진, 세션 관리, JSON 동적 설정 |
| **스케줄러** | `scheduler/` | APScheduler 기반 Cron/Interval 잡 관리 |

---

## 🛠️ 사전 지식 및 기술 스택

이 패키지를 활용하기 위해 아래 기술에 대한 기본 이해가 필요합니다.

### 백엔드
| 기술 | 버전 | 역할 | 학습 링크 |
|---|---|---|---|
| **Python** | 3.9+ | 런타임 | [공식 문서](https://docs.python.org/ko/3/) |
| **FastAPI** | 0.100+ | REST API 서버 프레임워크 | [공식 문서](https://fastapi.tiangolo.com/ko/) |
| **SQLAlchemy** | 2.0+ | ORM (데이터베이스 모델 관리) | [공식 문서](https://docs.sqlalchemy.org/) |
| **Pydantic** | 2.0+ | 데이터 검증 및 설정 관리 | [공식 문서](https://docs.pydantic.dev/) |
| **APScheduler** | 3.10+ | 백그라운드 스케줄 작업 | [공식 문서](https://apscheduler.readthedocs.io/) |
| **JWT** | — | 사용자 인증 토큰 방식 | [jwt.io 소개](https://jwt.io/introduction) |
| **Google OAuth 2.0** | — | 소셜 로그인 표준 | [Google 가이드](https://developers.google.com/identity/protocols/oauth2) |

### 인프라 & 도구
| 기술 | 역할 | 참고 |
|---|---|---|
| **Git / GitHub** | 소스 버전 관리 및 협업 | [Git 기초](https://git-scm.com/book/ko/v2) |
| **Git Submodule** | 공통 패키지 프로젝트 간 공유 | [Submodule 가이드](https://git-scm.com/book/ko/v2/Git-%EB%8F%84%EA%B5%AC-%EC%84%9C%EB%B8%8C%EB%AA%A8%EB%93%88) |
| **python-dotenv** | 환경변수 `.env` 파일 관리 | — |
| **Gmail 앱 비밀번호** | 이메일 발송 인증 | [설정 방법](https://support.google.com/accounts/answer/185833) |
| **Telegram BotFather** | 텔레그램 봇 토큰 발급 | [@BotFather](https://t.me/BotFather) |

---

## 🚀 빠른 시작

### 1. 신규 프로젝트에 연결 (Git Submodule)

```bash
# 신규 프로젝트 루트에서 실행
git submodule add https://github.com/offroad0817/vm-common-core common_core
pip install -r common_core/requirements.txt

# 환경변수 설정
cp common_core/.env.example .env
# .env 파일을 열어 각 값 입력
```

> **팀원이 저장소를 클론할 경우:**
> ```bash
> git clone --recurse-submodules https://github.com/your/project.git
> ```

### 2. FastAPI 앱에 즉시 적용

```python
# app/api.py
from fastapi import FastAPI
from common_core.auth import get_current_active_user, get_admin_user
from common_core.db import Base, engine, get_db
from common_core.auth.models import User

# DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/me")
def get_my_info(current_user: User = Depends(get_current_active_user)):
    return {"email": current_user.email, "role": current_user.role}
```

### 3. 알림 발송

```python
from common_core.notifier import send_email, send_telegram_message

# 이메일 발송 (HTML 형식)
send_email(
    to_email="user@example.com",
    subject="[My App] 알림",
    body="<h1>안녕하세요!</h1><p>이메일 알림 테스트입니다.</p>",
    is_html=True,
)

# 텔레그램 메시지 발송
send_telegram_message("🚀 <b>배포 완료</b>\n서버가 정상 작동 중입니다.")
```

### 4. 스케줄러 등록

```python
from common_core.scheduler import BaseScheduler

def my_daily_task():
    print("매일 오전 7시 실행!")

class MyProjectScheduler(BaseScheduler):
    def register_jobs(self):
        self.add_cron_job(my_daily_task, job_id="daily_task", hour=7, minute=0)

# FastAPI lifespan 또는 main.py 에서
scheduler = MyProjectScheduler()
scheduler.start()
```

### 5. 도메인 모델 확장

```python
# my_project/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from common_core.db import Base, TimestampMixin

class MyDomainItem(Base, TimestampMixin):
    """created_at, updated_at이 자동으로 추가됩니다."""
    __tablename__ = "my_domain_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200), nullable=False)
    # ... 필요한 컬럼 추가
```

---

## 📁 디렉토리 구조

```
vm-common-core/
├── auth/
│   ├── __init__.py          # 공개 인터페이스
│   ├── jwt_handler.py       # JWT 발급, Google OAuth 검증
│   ├── guards.py            # FastAPI Depends 권한 가드
│   └── models.py            # User, RoleEnum, StatusEnum
├── notifier/
│   ├── __init__.py
│   ├── email.py             # Gmail SMTP 발송
│   └── telegram.py          # 텔레그램 Bot 발송
├── db/
│   ├── __init__.py
│   ├── database.py          # SQLAlchemy 엔진·세션·get_db()
│   ├── base_model.py        # TimestampMixin
│   └── settings.py          # JSON 동적 설정 관리
├── scheduler/
│   ├── __init__.py
│   └── base_scheduler.py   # BaseScheduler (APScheduler 래퍼)
├── docs/
│   ├── setup_guide.md       # 환경 세팅 가이드 (Gmail, Telegram, Google OAuth)
│   └── submodule_guide.md   # Git Submodule 관리 가이드
├── .env.example             # 환경변수 명세서
├── requirements.txt         # Python 의존성
└── README.md
```

---

## ⚙️ 환경변수 설정

`.env.example`을 참고하여 `.env` 파일을 작성합니다. 자세한 발급 방법은 [`docs/setup_guide.md`](docs/setup_guide.md)를 참고하세요.

| 변수명 | 필수 | 설명 |
|---|---|---|
| `JWT_SECRET_KEY` | ✅ | JWT 서명 비밀키 (32자 이상 임의 문자열) |
| `GOOGLE_CLIENT_ID` | ✅ | Google OAuth 클라이언트 ID |
| `MAIL_USER` | ✅ | Gmail 계정 주소 |
| `MAIL_PASSWORD` | ✅ | Gmail 앱 비밀번호 (일반 비밀번호 아님) |
| `TELEGRAM_BOT_TOKEN` | ✅ | @BotFather 발급 토큰 |
| `TELEGRAM_CHAT_ID` | ✅ | 수신 채팅방 ID |
| `DATABASE_URL` | ✅ | DB 연결 문자열 (기본: sqlite:///./app.db) |
| `MAIL_SENDER_NAME` | — | 발신자 표시 이름 (기본: "System") |
| `MAIL_CC_DEFAULT` | — | 기본 참조자 이메일 |
| `DEBUG` | — | true 설정 시 Google 토큰 미검증 (개발 전용) |

---

## 🔄 업데이트 관리

공통 패키지가 개선된 경우 각 프로젝트에서 아래 명령으로 최신 버전을 반영합니다.

```bash
# 프로젝트 루트에서 실행
git submodule update --remote common_core
git add common_core
git commit -m "chore: 공통 패키지 업데이트 반영"
```

---

## 📝 변경 이력

| 버전 | 날짜 | 내용 |
|---|---|---|
| v1.0.0 | 2026-04-13 | 최초 릴리스 — auth, notifier, db, scheduler 분리 |

---

> **출처**: VectorMoon AI 자동매매 플랫폼 (`stock_analyst`) 공통 모듈에서 분리
