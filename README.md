# 교회 회계 웹 백엔드

이 프로젝트는 교회 회계 웹 애플리케이션을 위한 백엔드 서버입니다. 현재 개발이 진행 중입니다.

## 🌟 주요 기술 스택

*   **프레임워크**: [FastAPI](https://fastapi.tiangolo.com/)
*   **데이터베이스**: [PostgreSQL](https://www.postgresql.org/) ([SQLAlchemy](https://www.sqlalchemy.org/)와 [Alembic](https://alembic.sqlalchemy.org/)으로 관리)
*   **의존성 관리**: [uv](https://github.com/astral-sh/uv)
*   **인증**: Passlib를 사용한 패스워드 해싱과 JWT
*   **의존성 주입**: [dependency-injector](https://python-dependency-injector.ets-labs.org/)

## 📂 프로젝트 구조

이 프로젝트는 도메인 중심의 구조를 따릅니다:

```
├── alembic/              # 데이터베이스 마이그레이션 스크립트
├── src/
│   ├── main/
│   │   ├── common/         # 공통 유틸리티 (DB, 보안, 설정)
│   │   ├── domain/         # 핵심 비즈니스 로직 및 엔티티
│   │   │   ├── member/
│   │   │   ├── organization/
│   │   │   └── ledger/
│   │   └── main.py         # FastAPI 애플리케이션 진입점
│   └── tests/              # 테스트 코드
├── .env.default          # 기본 환경 변수
├── alembic.ini           # Alembic 설정
├── Dockerfile            # 컨테이너화 설정
└── pyproject.toml        # 프로젝트 메타데이터 및 의존성
```

## 🚀 시작하기

### 사전 요구사항

-   Python 3.14+
-   [uv](https://github.com/astral-sh/uv) 설치 (`pip install uv`)
-   실행 중인 PostgreSQL 인스턴스

### 설치 방법

1.  **리포지토리 클론:**
    ```bash
    git clone https://github.com/ehrl1225/ChurchAccountingWebBackend.git
    ```

2.  **가상 환경 생성 및 의존성 설치:**
    ```bash
    uv sync
    ```

3.  **환경 변수 설정:**
    `.env.default` 파일을 복사하여 `.env` 파일을 생성하고, `DATABASE_URL`을 포함한 값들을 수정합니다.
    ```bash
    cp .env.default .env
    ```

### 데이터베이스 마이그레이션

최신 데이터베이스 스키마를 적용하려면 다음을 실행하세요:
```bash
alembic upgrade head
```

### 서버 실행

개발 서버를 실행하려면:
```bash
export PYTHONPATH="$PWD/src/main:$PWD"
uvicorn src.main.main:app --reload --host 0.0.0.0 --port 8000
```

API 문서는 [http://localhost:8000/docs](http://localhost:8000/docs)에서 확인할 수 있습니다.
