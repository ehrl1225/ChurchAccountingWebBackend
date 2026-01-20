# Church Accounting Web - 재정 관리 플랫폼

<p align="center">
  <strong>현대 교회를 위한 투명하고 효율적인 재정 관리 솔루션</strong>
</p>
<p align="center">
    <img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python 3.12+">
    <img src="https://img.shields.io/badge/Framework-FastAPI-05998b.svg" alt="FastAPI">
    <img src="https://img.shields.io/badge/Database-PostgreSQL-336791.svg" alt="PostgreSQL">
    <img src="https://img.shields.io/badge/ORM-SQLAlchemy-c42e1a.svg" alt="SQLAlchemy">
    <img src="https://img.shields.io/badge/infra-Docker-2496ed.svg" alt="Docker">
</p>

---

## 📖 프로젝트 개요

**Church Accounting Web**은 소규모부터 중대형 교회까지, 모든 교회가 재정을 투명하고 체계적으로 관리할 수 있도록 돕는 웹 기반 백엔드 플랫폼입니다. 복잡한 회계 업무를 단순화하고, 실시간 협업을 지원하며, 모든 재정 기록을 안전하게 보관하여 교회의 건강한 재정 운영을 목표로 합니다.

이 프로젝트는 포트폴리오 목적으로, 최신 웹 기술과 견고한 백엔드 아키텍처 설계를 적용하여 개발되었습니다.

## ✨ 주요 기능 (Key Features)

### 1. 다중 조직 및 역할 기반 권한 관리 (Multi-Tenancy & RBAC)
- **조직 생성 및 관리**: 각 교회는 독립된 `조직(Organization)`을 생성하여 재정 정보를 완벽하게 분리하고 관리할 수 있습니다.
- **사용자 초대 및 역할 부여**: `소유자(Owner)`, `관리자(Admin)`, `일반 멤버(Member)` 등 역할에 따라 기능 접근 권한을 세분화합니다. 관리자는 이메일을 통해 새로운 멤버를 안전하게 초대할 수 있습니다.
- **실시간 초대 알림**: **Server-Sent Events (SSE)** 기술을 활용하여, 초대받은 사용자는 페이지 새로고침 없이 실시간으로 초대 알림을 수신하고 수락/거절할 수 있습니다.

### 2. 지능형 회계 장부 (Intelligent Ledger)
- **수입/지출 기록**: 모든 재정 거래(수입/지출)를 간편하게 기록하고, 거래 내역, 날짜, 금액, 관련 인물 등 상세 정보를 관리합니다.
- **거래 항목 분류**: '십일조', '감사헌금', '건축헌금' 등 교회 재정에 맞는 계정과목을 자유롭게 설정하여 거래를 체계적으로 분류하고 분석할 수 있습니다.
- **재정 요약 및 검색**: 특정 기간, 계정과목 등 다양한 조건으로 재정 데이터를 필터링하고 검색할 수 있으며, 해당 기간의 재정 요약 리포트를 제공받을 수 있습니다.

### 3. 비동기 대용량 데이터 처리 및 리포팅
- **Excel 대량 등록**: 수백, 수천 건의 거래 내역을 **Excel 템플릿**을 통해 한 번에 업로드할 수 있습니다. 업로드 작업은 **백그라운드에서 비동기(Asynchronous)**로 처리되어, 서버의 부하를 최소화 합니다.
- **실시간 작업 상태 추적**: Excel 업로드 또는 다운로드 같은 오래 걸리는 작업의 진행 상태(대기, 진행 중, 완료, 실패)를 **SSE**를 통해 프론트엔드에 실시간으로 브로드캐스팅하여 사용자 경험을 향상시킵니다.
- **문서 리포트 생성**: 특정 월의 재정 결산 보고서를 **MS Word (.docx) 형식**으로 동적으로 생성하고 다운로드할 수 있습니다.

### 4. 안전한 파일 관리 (Secure File Management)
- **영수증 및 증빙자료 첨부**: 각 거래 기록에 영수증 이미지나 관련 파일을 안전하게 첨부할 수 있습니다.
- **Presigned URL 기반 파일 전송**: 클라이언트(브라우저)가 백엔드 서버를 거치지 않고 **AWS S3** 같은 클라우드 스토리지에 직접 파일을 업로드/다운로드하도록 **Presigned URL**을 발급합니다. 이를 통해 서버 부하를 줄이고 데이터 전송의 보안과 효율성을 극대화합니다.

## 🏛️ 아키텍처 및 기술적 결정

이 프로젝트는 확장성, 유지보수성, 그리고 개발 효율성을 높이기 위해 다음과 같은 아키텍처 원칙과 기술을 적용했습니다.

- **도메인 주도 설계 (Domain-Driven Design) 구조**: `member`, `organization`, `ledger` 등 핵심 비즈니스 로직을 각 도메인별로 명확하게 분리했습니다. 이를 통해 코드의 응집도를 높이고, 복잡한 비즈니스 요구사항을 보다 쉽게 모델링하고 확장할 수 있습니다.

- **FastAPI 기반의 비동기 처리**: FastAPI의 네이티브 `async/await` 지원을 적극 활용하여 모든 API 엔드포인트와 데이터베이스 접근을 비동기적으로 처리합니다. 이는 대규모 트래픽 환경에서도 높은 처리량과 빠른 응답 속도를 보장하며, 실시간 알림과 같은 기능을 효율적으로 구현하는 기반이 됩니다.

- **의존성 주입 (Dependency Injection)을 통한 결합도 최소화**: `dependency-injector` 라이브러리를 사용해 서비스, 리포지토리 등의 의존성을 외부에서 주입합니다. 이는 각 컴포넌트의 결합도를 낮춰 단위 테스트를 용이하게 하고, 기능 변경 및 확장에 유연하게 대처할 수 있도록 합니다.

- **데이터 무결성 및 버전 관리**:
  - **Pydantic**: 모든 API 요청/응답 및 환경 변수 설정에 Pydantic 모델을 적용하여 런타임 이전에 데이터의 유효성을 검증하고, 코드의 안정성을 높입니다.
  - **SQLAlchemy & Alembic**: ORM을 통해 Python 코드로 데이터베이스 스키마를 관리하고, Alembic으로 모든 스키마 변경 이력을 체계적으로 버전 관리하여 팀원 간의 협업과 배포를 원활하게 합니다.

- **Docker 기반의 재현 가능한 개발 환경**: `Docker Compose`를 통해 데이터베이스(PostgreSQL), 캐시/메시지 큐(Redis), 웹 서버, 백그라운드 워커 등 모든 서비스를 컨테이너화했습니다. 이를 통해 어떤 환경에서든 `docker-compose up` 명령어 하나로 완벽하게 동일한 개발 및 테스트 환경을 재현할 수 있습니다.

## ⚙️ 기술 스택 (Tech Stack)

| 구분 | 기술 | 설명 |
|---|---|---|
| **Web Framework** | [FastAPI](https://fastapi.tiangolo.com/) | Python 3.8+ 기반의 고성능 ASGI 웹 프레임워크. 비동기 처리, 자동 API 문서 생성. |
| **Database** | [PostgreSQL](https://www.postgresql.org/) | 안정성과 확장성이 뛰어난 오픈소스 관계형 데이터베이스. |
| **ORM & Migration** | [SQLAlchemy](https://www.sqlalchemy.org/), [Alembic](https://alembic.sqlalchemy.org/) | Pythonic한 ORM 및 데이터베이스 스키마 버전 관리 도구. |
| **Async Task Queue**| [Redis](https://redis.io/), [RQ (Redis Queue)](https://python-rq.org/) | 대용량 파일 처리 등 오래 걸리는 작업을 위한 비동기 태스크 큐. |
| **Package Manager**| [uv](https://github.com/astral-sh/uv) | Rust 기반의 매우 빠른 Python 패키지 설치 및 관리 도구. |
| **Containerization**| [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/) | 서비스 컨테이너화 및 개발 환경 일관성 유지. |
| **Dependency Injection**| [dependency-injector](https://python-dependency-injector.ets-labs.org/) | 느슨한 결합(Loose Coupling) 및 테스트 용이성 확보. |
| **Data Validation**| [Pydantic](https://docs.pydantic.dev/latest/) | API 데이터 유효성 검증 및 강력한 타입 힌팅. |
| **Authentication** | Passlib (bcrypt), JWT | 안전한 비밀번호 해싱 및 stateless 인증. |
| **Cloud Storage** | Boto3 (for AWS S3) | Presigned URL을 통한 안전한 파일 업로드/다운로드. |


## 🚀 시작하기

두 가지 방법으로 프로젝트를 시작할 수 있습니다. Docker를 사용하는 것을 적극 권장합니다.

### 1. Docker를 이용한 실행 (권장)
1.  **Docker Compose 서비스 활성화:** `docker-compose.yaml` 파일을 열고 주석 처리된 `web`, `worker` 서비스의 주석을 해제합니다.
2.  **환경 변수 설정:** 프로젝트 루트에 `.env` 파일을 생성하고 아래 템플릿을 복사하여 환경에 맞게 수정합니다.
    ```env
    PROFILE=dev
    SECRET_KEY=your_strong_secret_key
    SMTP_PASS=your_smtp_password
    JWT_SECRET_KEY=your_jwt_secret_key
    JWT_ALGORITHM=HS256
    SERVER_PEPPER=your_server_pepper
    AWS_ACCESS_KEY_ID=your_aws_access_key
    AWS_SECRET_ACCESS_KEY=your_aws_secret_key
    REGION_NAME=ap-northeast-2
    BUCKET_NAME=your-s3-bucket-name
    REDIS_PASSWORD=your_redis_password
    ```
3.  **Docker Compose 실행:**
    ```bash
    docker-compose up --build
    ```
4.  **데이터베이스 마이그레이션 (최초 1회):** 새 터미널에서 아래 명령을 실행합니다.
    ```bash
    docker-compose run --rm web alembic upgrade head
    ```

### 2. 로컬 환경에서 직접 실행
1.  **사전 요구사항:** Python 3.12+, `uv`, PostgreSQL, Redis
2.  **의존성 설치:**
    ```bash
    uv sync
    ```
3.  **환경 변수 설정:** 위와 동일하게 `.env` 파일을 생성하고 설정합니다.
4.  **데이터베이스 마이그레이션:**
    ```bash
    uv run alembic upgrade head
    ```
5.  **서버 및 워커 실행:** (두 개의 터미널에서 각각 실행)
    ```bash
    # 터미널 1: FastAPI 웹 서버
    uvicorn src.main.main:app --reload --host 0.0.0.0 --port 8000

    # 터미널 2: RQ 워커
    uv run src/main/common/redis/worker.py
    ```

## 🧪 테스트
프로젝트 루트에서 다음 명령을 실행하여 모든 테스트를 수행할 수 있습니다.
```bash
pytest
```

## 📚 API 문서
서버가 실행 중일 때, 브라우저에서 [http://localhost:8000/docs](http://localhost:8000/docs)로 접속하면 자동 생성된 Swagger UI API 문서를 통해 모든 API를 테스트해볼 수 있습니다.

## 🌱 향후 개선 과제 (Future Work)
- **고급 리포팅 및 대시보드**: 연간/분기별 재정 보고서, 다양한 차트를 포함한 시각적 대시보드 기능 추가.
- **예산 관리**: 연간/월간 예산을 설정하고 지출과 비교 분석하는 기능.
- **감사 추적 (Audit Trail)**: 모든 재정 데이터의 변경 이력을 추적하여 투명성을 강화하는 기능.
- **다국어 지원 (i18n)**: 다양한 언어 환경을 지원.
