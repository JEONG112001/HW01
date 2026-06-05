# HW01: PostgreSQL 기반 사회복무요원 복무관리 개선 시스템

## 1. 프로젝트 개요

본 프로젝트는 데이터베이스 과제를 위해 제작한 Flask + PostgreSQL 기반 웹 서비스입니다.
복무기관담당자 관점에서 사회복무요원의 근무상황과 출근점검 상태를 관리할 수 있도록 설계했습니다.

과거 병무청 민원 제안 경험을 바탕으로 다음 개선 아이디어를 반영했습니다.

- 근무상황 종별, 요원별, 기간별 조회
- 출근점검 시 일일복무상황부 수기 작성 여부 확인
- 최근 출근점검일이 오래된 근무지 우선 조회
- 통상 근무시간 외 근무편성 및 승인 여부 확인

> 주의: 본 프로젝트의 데이터는 모두 과제용 가상 데이터이며 실제 개인정보를 포함하지 않습니다.

---

## 2. 사용 기술

- Python Flask
- PostgreSQL
- psycopg2
- HTML / CSS

---

## 3. 주요 기능

1. 근무지 등록 및 조회
2. 사회복무요원 등록 및 조회
3. 근무상황 등록 및 검색
4. 출근점검 등록
5. 최근 점검일 오래된 근무지 조회
6. 통상 근무시간 외 근무편성 조회

---

## 4. 데이터베이스 릴레이션

본 프로젝트는 총 4개의 릴레이션을 사용합니다.

| 릴레이션 | 설명 |
|---|---|
| `workplaces` | 복무기관 담당자가 관리하는 근무지 정보 |
| `service_members` | 사회복무요원 기본 정보 |
| `duty_records` | 연가, 병가, 지각, 조퇴, 외출, 유연근무 등 근무상황 기록 |
| `check_visits` | 출근점검 기록 및 일일복무상황부 수기 작성 확인 여부 |

관계 구조는 다음과 같습니다.

```text
workplaces 1 ─── N service_members
workplaces 1 ─── N check_visits
service_members 1 ─── N duty_records
```

---

## 5. 실행 방법

### 5-1. PostgreSQL 데이터베이스 생성

```sql
CREATE DATABASE hw01_db;
```

### 5-2. 테이블 생성

```bash
psql -U postgres -d hw01_db -f schema.sql
```

### 5-3. 샘플 데이터 입력

```bash
psql -U postgres -d hw01_db -f seed.sql
```

### 5-4. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 5-5. 환경변수 설정

프로젝트 폴더에 `.env` 파일을 만들고 아래처럼 작성합니다.

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hw01_db
DB_USER=postgres
DB_PASSWORD=본인_PostgreSQL_비밀번호
```

`.env` 파일은 개인정보가 포함될 수 있으므로 GitHub에 올리지 않습니다.

### 5-6. Flask 실행

```bash
python app.py
```

브라우저에서 아래 주소로 접속합니다.

```text
http://127.0.0.1:5000
```

---

## 6. Query 예시

### 근무상황 종류별 조회

```sql
SELECT *
FROM duty_records
WHERE duty_type = '연가';
```

### 최근 점검일 오래된 근무지 조회

```sql
SELECT workplace_id, workplace_name, service_field, last_check_date
FROM workplaces
ORDER BY last_check_date ASC NULLS FIRST;
```

### 통상 근무시간 외 근무편성 조회

```sql
SELECT
    sm.name,
    w.workplace_name,
    dr.duty_type,
    dr.duty_date,
    dr.start_time,
    dr.end_time,
    w.normal_start_time,
    w.normal_end_time
FROM duty_records dr
JOIN service_members sm ON dr.member_id = sm.member_id
JOIN workplaces w ON sm.workplace_id = w.workplace_id
WHERE dr.start_time < w.normal_start_time
   OR dr.end_time > w.normal_end_time;
```

---

## 7. Transaction 적용

출근점검 저장 기능에서 트랜잭션을 사용했습니다.

출근점검 저장 시 다음 두 작업이 동시에 처리됩니다.

1. `check_visits` 테이블에 출근점검 기록 저장
2. `workplaces` 테이블의 `last_check_date` 갱신

두 작업이 모두 성공해야 `COMMIT`하고, 중간에 오류가 발생하면 `ROLLBACK`합니다.

```text
출근점검 기록 저장 + 최근 점검일 갱신 = 하나의 업무 단위
```

이를 통해 데이터가 일부만 저장되는 문제를 방지할 수 있습니다.

---

## 8. 제출 안내

GitHub에는 다음 파일을 포함합니다.

- `app.py`
- `db.py`
- `schema.sql`
- `seed.sql`
- `requirements.txt`
- `README.md`
- `templates/`
- `static/`

GitHub에는 다음 파일을 올리지 않습니다.

- `.env`
- `venv/`
- `__pycache__/`
- 실제 개인정보가 포함된 파일
