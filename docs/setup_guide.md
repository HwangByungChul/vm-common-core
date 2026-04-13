# 환경 세팅 가이드

공통 패키지 사용에 필요한 외부 서비스 발급 및 설정 방법을 단계별로 안내합니다.

---

## 1. JWT 비밀키 생성

터미널에서 아래 명령으로 안전한 랜덤 키를 생성합니다.

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

생성된 값을 `.env`의 `JWT_SECRET_KEY`에 입력합니다.

---

## 2. Google OAuth 2.0 클라이언트 ID 발급

1. [Google Cloud Console](https://console.cloud.google.com/) 접속 → 프로젝트 생성
2. **API 및 서비스** → **OAuth 동의 화면** 설정
   - 사용자 유형: **외부** 선택
   - 앱 이름, 지원 이메일 입력
3. **사용자 인증 정보** → **사용자 인증 정보 만들기** → **OAuth 클라이언트 ID**
   - 애플리케이션 유형: **웹 애플리케이션**
   - 승인된 JavaScript 원본: `http://localhost:3000`
   - 승인된 리디렉션 URI: `http://localhost:8080/api/auth/google`
4. 생성된 **클라이언트 ID**를 `.env`의 `GOOGLE_CLIENT_ID`에 입력

> **개발 환경**: `GOOGLE_CLIENT_ID`를 비워두거나 `DEBUG=true`로 설정하면 이메일 문자열로 직접 로그인 가능합니다.

---

## 3. Gmail 앱 비밀번호 발급

> ⚠️ **일반 Gmail 비밀번호가 아닌 앱 비밀번호**를 사용해야 합니다.

1. [Google 계정](https://myaccount.google.com) → **보안** 탭
2. **2단계 인증** 활성화 (미활성 시 앱 비밀번호 메뉴가 보이지 않음)
3. **앱 비밀번호** → 앱 선택: **기타(직접 입력)** → 이름 입력 (예: "MyApp")
4. 생성된 **16자리 비밀번호**를 `.env`의 `MAIL_PASSWORD`에 입력

```env
MAIL_USER=your-gmail@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop    # 공백 포함 16자 그대로 입력
```

---

## 4. 텔레그램 Bot 생성 및 Chat ID 확인

### Bot 토큰 발급
1. 텔레그램에서 **@BotFather** 검색 → 대화 시작
2. `/newbot` 명령 입력 → 봇 이름과 아이디(@xxx_bot) 입력
3. 발급된 **HTTP API 토큰**을 `.env`의 `TELEGRAM_BOT_TOKEN`에 입력

### Chat ID 확인
1. 텔레그램에서 **@userinfobot** 검색 → `/start` 전송
2. 응답받은 **Id** 값을 `.env`의 `TELEGRAM_CHAT_ID`에 입력

> **그룹 채팅방 사용 시**: 봇을 그룹에 초대한 후 `https://api.telegram.org/bot<TOKEN>/getUpdates`에 접속, `chat.id` 값을 확인합니다. (그룹 ID는 음수값)

---

## 5. 데이터베이스 설정

### 개발 환경 (SQLite)
별도 설치 없이 파일 기반으로 동작합니다.
```env
DATABASE_URL=sqlite:///./app.db
```

### 프로덕션 환경 (PostgreSQL)
```bash
# PostgreSQL 설치 후
pip install psycopg2-binary
```
```env
DATABASE_URL=postgresql://username:password@localhost:5432/mydbname
```
