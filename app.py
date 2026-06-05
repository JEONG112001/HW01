from flask import Flask, render_template, request, redirect, url_for, flash
from db import fetch_all, execute, get_conn

app = Flask(__name__)
app.secret_key = "dev-secret-key"

DUTY_TYPES = [
    "연가", "병가", "지각", "조퇴", "외출", "출장", "결근", "공가", "교육", "유연근무", "근무시간변경"
]


@app.route("/")
def index():
    counts = {
        "workplaces": fetch_all("SELECT COUNT(*) AS cnt FROM workplaces")[0]["cnt"],
        "members": fetch_all("SELECT COUNT(*) AS cnt FROM service_members")[0]["cnt"],
        "duties": fetch_all("SELECT COUNT(*) AS cnt FROM duty_records")[0]["cnt"],
        "checks": fetch_all("SELECT COUNT(*) AS cnt FROM check_visits")[0]["cnt"],
    }
    return render_template("index.html", counts=counts)


@app.route("/workplaces", methods=["GET", "POST"])
def workplaces():
    if request.method == "POST":
        execute(
            """
            INSERT INTO workplaces (workplace_name, service_field, normal_start_time, normal_end_time)
            VALUES (%s, %s, %s, %s)
            """,
            (
                request.form["workplace_name"],
                request.form.get("service_field"),
                request.form.get("normal_start_time") or "09:00",
                request.form.get("normal_end_time") or "18:00",
            ),
        )
        flash("근무지가 등록되었습니다.")
        return redirect(url_for("workplaces"))

    rows = fetch_all("SELECT * FROM workplaces ORDER BY workplace_id")
    return render_template("workplaces.html", workplaces=rows)


@app.route("/members", methods=["GET", "POST"])
def members():
    workplaces_rows = fetch_all("SELECT workplace_id, workplace_name FROM workplaces ORDER BY workplace_name")
    if request.method == "POST":
        execute(
            """
            INSERT INTO service_members (name, birth_date, workplace_id, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                request.form["name"],
                request.form.get("birth_date") or None,
                request.form.get("workplace_id") or None,
                request.form.get("start_date") or None,
                request.form.get("end_date") or None,
                request.form.get("status") or "복무중",
            ),
        )
        flash("사회복무요원이 등록되었습니다.")
        return redirect(url_for("members"))

    rows = fetch_all(
        """
        SELECT sm.*, w.workplace_name
        FROM service_members sm
        LEFT JOIN workplaces w ON sm.workplace_id = w.workplace_id
        ORDER BY sm.member_id
        """
    )
    return render_template("members.html", members=rows, workplaces=workplaces_rows)


@app.route("/duty-records", methods=["GET", "POST"])
def duty_records():
    members_rows = fetch_all(
        """
        SELECT sm.member_id, sm.name, w.workplace_name
        FROM service_members sm
        LEFT JOIN workplaces w ON sm.workplace_id = w.workplace_id
        ORDER BY sm.name
        """
    )

    if request.method == "POST":
        execute(
            """
            INSERT INTO duty_records
            (member_id, duty_type, duty_subtype, duty_date, start_time, end_time, reason, workplace_approved, military_office_approved)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                request.form["member_id"],
                request.form["duty_type"],
                request.form.get("duty_subtype"),
                request.form["duty_date"],
                request.form.get("start_time") or None,
                request.form.get("end_time") or None,
                request.form.get("reason"),
                "workplace_approved" in request.form,
                "military_office_approved" in request.form,
            ),
        )
        flash("근무상황 기록이 등록되었습니다.")
        return redirect(url_for("duty_records"))

    duty_type = request.args.get("duty_type", "")
    member_id = request.args.get("member_id", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    query = """
        SELECT dr.*, sm.name, w.workplace_name
        FROM duty_records dr
        JOIN service_members sm ON dr.member_id = sm.member_id
        LEFT JOIN workplaces w ON sm.workplace_id = w.workplace_id
        WHERE 1=1
    """
    params = []
    if duty_type:
        query += " AND dr.duty_type = %s"
        params.append(duty_type)
    if member_id:
        query += " AND dr.member_id = %s"
        params.append(member_id)
    if start_date:
        query += " AND dr.duty_date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND dr.duty_date <= %s"
        params.append(end_date)
    query += " ORDER BY dr.duty_date DESC, dr.record_id DESC"

    rows = fetch_all(query, params)
    return render_template(
        "duty_records.html",
        records=rows,
        members=members_rows,
        duty_types=DUTY_TYPES,
        filters={"duty_type": duty_type, "member_id": member_id, "start_date": start_date, "end_date": end_date},
    )


@app.route("/check-visits", methods=["GET", "POST"])
def check_visits():
    workplaces_rows = fetch_all("SELECT workplace_id, workplace_name FROM workplaces ORDER BY workplace_name")

    if request.method == "POST":
        workplace_id = request.form["workplace_id"]
        check_date = request.form["check_date"]
        checked_by = request.form.get("checked_by")
        manual_log_checked = "manual_log_checked" in request.form
        result = request.form.get("result") or "확인"
        memo = request.form.get("memo")

        # 트랜잭션: 출근점검 기록 저장 + 근무지 최근 점검일 갱신
        conn = get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO check_visits
                        (workplace_id, check_date, checked_by, manual_log_checked, result, memo)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (workplace_id, check_date, checked_by, manual_log_checked, result, memo),
                    )
                    cur.execute(
                        """
                        UPDATE workplaces
                        SET last_check_date = %s
                        WHERE workplace_id = %s
                        """,
                        (check_date, workplace_id),
                    )
            flash("출근점검 기록이 저장되고 최근 점검일이 갱신되었습니다.")
        except Exception as e:
            conn.rollback()
            flash(f"저장 중 오류가 발생했습니다: {e}")
        finally:
            conn.close()
        return redirect(url_for("check_visits"))

    rows = fetch_all(
        """
        SELECT cv.*, w.workplace_name
        FROM check_visits cv
        JOIN workplaces w ON cv.workplace_id = w.workplace_id
        ORDER BY cv.check_date DESC, cv.check_id DESC
        """
    )
    return render_template("check_visits.html", checks=rows, workplaces=workplaces_rows)


@app.route("/reports")
def reports():
    old_checks = fetch_all(
        """
        SELECT workplace_id, workplace_name, service_field, last_check_date
        FROM workplaces
        ORDER BY last_check_date ASC NULLS FIRST, workplace_name ASC
        """
    )

    outside_hours = fetch_all(
        """
        SELECT
            dr.record_id,
            dr.duty_date,
            dr.duty_type,
            dr.start_time,
            dr.end_time,
            dr.workplace_approved,
            dr.military_office_approved,
            sm.name,
            w.workplace_name,
            w.normal_start_time,
            w.normal_end_time
        FROM duty_records dr
        JOIN service_members sm ON dr.member_id = sm.member_id
        JOIN workplaces w ON sm.workplace_id = w.workplace_id
        WHERE dr.start_time IS NOT NULL
          AND dr.end_time IS NOT NULL
          AND (dr.start_time < w.normal_start_time OR dr.end_time > w.normal_end_time)
        ORDER BY dr.duty_date DESC
        """
    )
    return render_template("reports.html", old_checks=old_checks, outside_hours=outside_hours)


if __name__ == "__main__":
    app.run(debug=True)
