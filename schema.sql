-- HW01: PostgreSQL 기반 사회복무요원 복무관리 개선 시스템
-- 실제 개인정보가 아닌 과제용 가상 데이터 사용을 전제로 합니다.

DROP TABLE IF EXISTS check_visits CASCADE;
DROP TABLE IF EXISTS duty_records CASCADE;
DROP TABLE IF EXISTS service_members CASCADE;
DROP TABLE IF EXISTS workplaces CASCADE;

CREATE TABLE workplaces (
    workplace_id SERIAL PRIMARY KEY,
    workplace_name VARCHAR(100) NOT NULL,
    service_field VARCHAR(100),
    normal_start_time TIME DEFAULT '09:00',
    normal_end_time TIME DEFAULT '18:00',
    last_check_date DATE
);

CREATE TABLE service_members (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    birth_date DATE,
    workplace_id INT REFERENCES workplaces(workplace_id) ON DELETE SET NULL,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT '복무중'
);

CREATE TABLE duty_records (
    record_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES service_members(member_id) ON DELETE CASCADE,
    duty_type VARCHAR(50) NOT NULL,
    duty_subtype VARCHAR(50),
    duty_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    reason TEXT,
    workplace_approved BOOLEAN DEFAULT FALSE,
    military_office_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE check_visits (
    check_id SERIAL PRIMARY KEY,
    workplace_id INT REFERENCES workplaces(workplace_id) ON DELETE CASCADE,
    check_date DATE NOT NULL,
    checked_by VARCHAR(50),
    manual_log_checked BOOLEAN DEFAULT FALSE,
    result VARCHAR(20) DEFAULT '확인',
    memo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
