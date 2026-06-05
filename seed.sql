-- 과제용 가상 샘플 데이터입니다. 실제 개인정보를 포함하지 않습니다.

INSERT INTO workplaces (workplace_name, service_field, normal_start_time, normal_end_time, last_check_date) VALUES
('복지관리과', '일반행정지원', '09:00', '18:00', '2026-06-01'),
('안전총괄과', '재난안전업무지원', '09:00', '18:00', '2026-05-28'),
('소흘노인복지센터', '사회복지시설운영지원', '09:00', '18:00', '2026-05-20'),
('열린지역아동센터', '아동복지시설지원', '10:00', '19:00', NULL);

INSERT INTO service_members (name, birth_date, workplace_id, start_date, end_date, status) VALUES
('김민수', '2004-01-15', 1, '2025-01-02', '2026-10-01', '복무중'),
('이준호', '2003-05-22', 3, '2025-03-10', '2026-12-09', '복무중'),
('박지훈', '2004-09-08', 4, '2025-06-01', '2027-02-28', '복무중');

INSERT INTO duty_records (member_id, duty_type, duty_subtype, duty_date, start_time, end_time, reason, workplace_approved, military_office_approved) VALUES
(1, '연가', '', '2026-06-10', '09:00', '18:00', '개인 사유', true, false),
(2, '지각', '', '2026-06-11', '09:30', '18:00', '교통 지연', true, false),
(3, '유연근무', '근무시간변경', '2026-06-12', '11:00', '20:00', '시설 프로그램 운영 시간 조정', true, true),
(1, '근무시간변경', '조기근무', '2026-06-14', '07:00', '16:00', '행사 지원', true, false);

INSERT INTO check_visits (workplace_id, check_date, checked_by, manual_log_checked, result, memo) VALUES
(1, '2026-06-01', '담당자A', true, '확인', '이상 없음'),
(3, '2026-05-20', '담당자A', false, '미흡', '일일복무상황부 수기 작성 확인 필요'),
(2, '2026-05-28', '담당자B', true, '확인', '이상 없음');
