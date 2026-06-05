# HW01: PostgreSQL 기반 공익요원 복무관리 개선 시스템

## 1. 프로젝트 개요
본 프로젝트는 데이터베이스 과제를 위해 제작한 Flask + PostgreSQL 기반 웹 서비스입니다.
복무기관 담당자 관점에서 근무상황과 출근점검 상태를 관리할 수 있도록 설계했습니다.

---
## 2. 실행 방법

### 2-1. PostgreSQL 데이터베이스 생성
```sql
CREATE DATABASE hw01_db;
```

### 2-2. 테이블 생성
```bash
psql -U postgres -d hw01_db -f schema.sql
```

### 2-3. 샘플 데이터 입력
```bash
psql -U postgres -d hw01_db -f seed.sql
```

### 2-4. Python 패키지 설치
```bash
pip install -r requirements.txt
```

### 2-5. 환경변수 설정
프로젝트 폴더에 `.env` 파일을 만들고 아래처럼 작성합니다.

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hw01_db
DB_USER=hw01_user
DB_PASSWORD=비밀번호
```

### 2-6. Flask 실행
```bash
python app.py
브라우저에서 아래 주소로 접속합니다.

```text
http://127.0.0.1:5000
``
