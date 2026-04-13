# Git Submodule 관리 가이드

공통 패키지를 Git Submodule로 여러 프로젝트에서 공유하고 관리하는 방법입니다.

---

## Submodule이란?

Git Submodule은 **하나의 Git 저장소 안에 다른 Git 저장소를 포함**시키는 기능입니다.
`vm-common-core`를 독립 저장소로 관리하고, 각 프로젝트에서는 이를 참조만 합니다.

```
my-project/
├── app/                ← 프로젝트 고유 코드
├── common_core/        ← vm-common-core 저장소 (submodule)
└── ...
```

---

## 자주 사용하는 명령어 모음

### 신규 프로젝트에 연결 (최초 1회)
```bash
git submodule add https://github.com/offroad0817/vm-common-core common_core
git commit -m "chore: 공통 패키지 submodule 연결"
```

### 저장소 클론 시 Submodule 함께 받기
```bash
# 방법 1: 클론할 때 한 번에
git clone --recurse-submodules https://github.com/your/project.git

# 방법 2: 클론 후 별도 초기화
git clone https://github.com/your/project.git
cd your-project
git submodule init
git submodule update
```

### 공통 패키지 최신 버전으로 업데이트
```bash
# common_core만 업데이트
git submodule update --remote common_core

# 변경사항 프로젝트에 반영
git add common_core
git commit -m "chore: 공통 패키지 v1.x.x 업데이트 반영"
```

### 공통 패키지 직접 수정 & 배포
```bash
# vm-common-core 저장소로 이동
cd /Users/jwpios/.gemini/antigravity/vm-common-core

# 코드 수정 후
git add .
git commit -m "fix: 이메일 모듈 수신자 표시 이름 기능 추가"
git push origin main

# 업데이트를 사용하는 각 프로젝트에서 위 "최신 버전으로 업데이트" 명령 실행
```

---

## 주의사항

> [!WARNING]
> **절대 `common_core/` 내부를 프로젝트에서 직접 수정하지 마세요.**
> submodule 내부를 직접 수정하면 해당 프로젝트에만 반영되고,
> 다른 프로젝트와 공통 저장소는 업데이트되지 않아 불일치가 발생합니다.
>
> 공통 코드 수정은 반드시 **vm-common-core 저장소**에서 직접 수정 후 push해야 합니다.

> [!TIP]
> `common_core/.gitignore`에 명시된 `.env` 파일은 git에 포함되지 않습니다.
> 각 프로젝트마다 `.env.example`을 복사하여 `.env`를 별도로 관리하세요.
