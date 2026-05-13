import os
import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = "bmcc-campusconnect-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")
SCHEMA = os.path.join(BASE_DIR, "schema.sql")


def get_db_connection():
    """Create a SQLite database connection and enable foreign keys."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create and seed the database if it does not already exist."""
    should_initialize: bool = not os.path.exists(DATABASE)

    if not should_initialize:
        try:
            conn = get_db_connection()
            table = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Student'"
            ).fetchone()
            conn.close()
            should_initialize = table is None
        except sqlite3.Error:
            should_initialize = True

    if should_initialize:
        with open(SCHEMA, "r", encoding="utf-8") as file:
            schema_sql = file.read()
        conn = get_db_connection()
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()


def fetch_one_or_404(query, params=()):
    conn = get_db_connection()
    row = conn.execute(query, params).fetchone()
    conn.close()
    if row is None:
        abort(404)
    return row


@app.route("/")
def index():
    conn = get_db_connection()
    stats = {
        "students": conn.execute("SELECT COUNT(*) FROM Student").fetchone()[0],
        "organizations": conn.execute("SELECT COUNT(*) FROM Organization").fetchone()[0],
        "events": conn.execute("SELECT COUNT(*) FROM Event").fetchone()[0],
        "rsvps": conn.execute("SELECT COUNT(*) FROM RSVP").fetchone()[0],
    }
    upcoming_events = conn.execute(
        """
        SELECT e.eventID, e.title, e.eventDate, e.startTime, e.location,
               e.category, o.orgName,
               COALESCE(r.confirmedCount, 0) AS confirmedCount,
               e.capacity - COALESCE(r.confirmedCount, 0) AS seatsLeft
        FROM Event e
        JOIN Organization o ON e.orgID = o.orgID
        LEFT JOIN (
            SELECT eventID, COUNT(*) AS confirmedCount
            FROM RSVP
            WHERE status = 'Confirmed'
            GROUP BY eventID
        ) r ON e.eventID = r.eventID
        ORDER BY e.eventDate, e.startTime
        LIMIT 6
        """
    ).fetchall()
    conn.close()
    return render_template("index.html", stats=stats, upcoming_events=upcoming_events)


# -------------------- Students CRUD --------------------
@app.route("/students")
def students():
    q = request.args.get("q", "").strip()
    conn = get_db_connection()
    if q:
        students = conn.execute(
            """
            SELECT * FROM Student
            WHERE firstName LIKE ? OR lastName LIKE ? OR BMCCemail LIKE ? OR major LIKE ?
            ORDER BY lastName, firstName
            """,
            (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"),
        ).fetchall()
    else:
        students = conn.execute(
            "SELECT * FROM Student ORDER BY lastName, firstName"
        ).fetchall()
    conn.close()
    return render_template("students.html", students=students, q=q)


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        emplid = request.form.get("emplid", "").strip()
        firstName = request.form.get("firstName", "").strip()
        lastName = request.form.get("lastName", "").strip()
        BMCCemail = request.form.get("BMCCemail", "").strip()
        major = request.form.get("major", "").strip()
        yearLevel = request.form.get("yearLevel", "").strip()

        if not firstName or not lastName or not BMCCemail:
            flash("First name, last name, and BMCC email are required.", "error")
            return render_template("student_form.html", student=request.form, action="Add")

        try:
            conn = get_db_connection()
            conn.execute(
                """
                INSERT INTO Student (firstName, lastName, BMCCemail, major, yearLevel)
                VALUES (?, ?, ?, ?, ?)
                """,
                (firstName, lastName, BMCCemail, major, yearLevel),
            )
            conn.commit()
            conn.close()
            flash("Student added successfully.", "success")
            return redirect(url_for("students"))
        except sqlite3.IntegrityError:
            flash("That BMCC email already exists.", "error")

    return render_template("student_form.html", student=None, action="Add")


@app.route("/students/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    student = fetch_one_or_404("SELECT * FROM Student WHERE studentID = ?", (id,))

    if request.method == "POST":
        emplid = request.form.get("emplid", "").strip()
        firstName = request.form.get("firstName", "").strip()
        lastName = request.form.get("lastName", "").strip()
        BMCCemail = request.form.get("BMCCemail", "").strip()
        major = request.form.get("major", "").strip()
        yearLevel = request.form.get("yearLevel", "").strip()  

        if not emplid or not firstName or not lastName or not BMCCemail:
            flash("EMPLID, first name, last name, and BMCC email are required.", "error")
            return render_template("student_form.html", student=request.form, action="Edit")         
        try:
            conn = get_db_connection()
            conn.execute(
            """
            UPDATE Student
            SET emplid = ?, firstName = ?, lastName = ?, BMCCemail = ?, major = ?, yearLevel = ?
            WHERE studentID = ?
            """,
            (emplid, firstName, lastName, BMCCemail, major, yearLevel, id)
)
            conn.commit()
            conn.close()
            flash("Student updated successfully.", "success")
            return redirect(url_for("students"))
        except sqlite3.IntegrityError:
            flash("That BMCC email already exists.", "error")

    return render_template("student_form.html", student=student, action="Edit")


@app.route("/students/delete/<int:id>", methods=["POST"])
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM Student WHERE studentID = ?", (id,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully.", "success")
    return redirect(url_for("students"))


# -------------------- Organizations CRUD --------------------
@app.route("/organizations")
def organizations():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    orgType = request.args.get("orgType", "").strip()

    conn = get_db_connection()
    categories = conn.execute(
        "SELECT DISTINCT category FROM Organization WHERE category IS NOT NULL AND category != '' ORDER BY category"
    ).fetchall()
    org_types = conn.execute(
        "SELECT DISTINCT orgType FROM Organization WHERE orgType IS NOT NULL AND orgType != '' ORDER BY orgType"
    ).fetchall()

    query = "SELECT * FROM Organization WHERE 1=1"
    params = []
    if q:
        query += " AND (orgName LIKE ? OR description LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])
    if category:
        query += " AND category = ?"
        params.append(category)
    if orgType:
        query += " AND orgType = ?"
        params.append(orgType)
    query += " ORDER BY orgName"

    organizations = conn.execute(query, params).fetchall()
    conn.close()
    return render_template(
        "organizations.html",
        organizations=organizations,
        categories=categories,
        org_types=org_types,
        q=q,
        selected_category=category,
        selected_orgType=orgType,
    )


@app.route("/organizations/add", methods=["GET", "POST"])
def add_organization():
    if request.method == "POST":
        orgName = request.form.get("orgName", "").strip()
        orgType = request.form.get("orgType", "").strip()
        category = request.form.get("category", "").strip()
        contactEmail = request.form.get("contactEmail", "").strip()
        description = request.form.get("description", "").strip()

        if not orgName or not orgType:
            flash("Organization name and type are required.", "error")
            return render_template("organization_form.html", organization=request.form, action="Add")

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO Organization (orgName, orgType, category, contactEmail, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (orgName, orgType, category, contactEmail, description),
        )
        conn.commit()
        conn.close()
        flash("Organization added successfully.", "success")
        return redirect(url_for("organizations"))

    return render_template("organization_form.html", organization=None, action="Add")


@app.route("/organizations/edit/<int:id>", methods=["GET", "POST"])
def edit_organization(id):
    organization = fetch_one_or_404("SELECT * FROM Organization WHERE orgID = ?", (id,))

    if request.method == "POST":
        orgName = request.form.get("orgName", "").strip()
        orgType = request.form.get("orgType", "").strip()
        category = request.form.get("category", "").strip()
        contactEmail = request.form.get("contactEmail", "").strip()
        description = request.form.get("description", "").strip()

        if not orgName or not orgType:
            flash("Organization name and type are required.", "error")
            return render_template("organization_form.html", organization=request.form, action="Edit")

        conn = get_db_connection()
        conn.execute(
            """
            UPDATE Organization
            SET orgName = ?, orgType = ?, category = ?, contactEmail = ?, description = ?
            WHERE orgID = ?
            """,
            (orgName, orgType, category, contactEmail, description, id),
        )
        conn.commit()
        conn.close()
        flash("Organization updated successfully.", "success")
        return redirect(url_for("organizations"))

    return render_template("organization_form.html", organization=organization, action="Edit")


@app.route("/organizations/delete/<int:id>", methods=["POST"])
def delete_organization(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM Organization WHERE orgID = ?", (id,))
    conn.commit()
    conn.close()
    flash("Organization deleted successfully. Related events and RSVPs were also removed.", "success")
    return redirect(url_for("organizations"))


# -------------------- Events CRUD --------------------
@app.route("/events")
def events():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    orgID = request.args.get("orgID", "").strip()

    conn = get_db_connection()
    categories = conn.execute("SELECT categoryName FROM EventCategory ORDER BY categoryName").fetchall()
    orgs = conn.execute("SELECT orgID, orgName FROM Organization ORDER BY orgName").fetchall()

    query = """
        SELECT e.*, o.orgName,
               COALESCE(r.confirmedCount, 0) AS confirmedCount,
               e.capacity - COALESCE(r.confirmedCount, 0) AS seatsLeft
        FROM Event e
        JOIN Organization o ON e.orgID = o.orgID
        LEFT JOIN (
            SELECT eventID, COUNT(*) AS confirmedCount
            FROM RSVP
            WHERE status = 'Confirmed'
            GROUP BY eventID
        ) r ON e.eventID = r.eventID
        WHERE 1=1
    """
    params = []
    if q:
        query += " AND (e.title LIKE ? OR e.description LIKE ? OR e.location LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])
    if category:
        query += " AND e.category = ?"
        params.append(category)
    if orgID:
        query += " AND e.orgID = ?"
        params.append(orgID)
    query += " ORDER BY e.eventDate, e.startTime"

    events = conn.execute(query, params).fetchall()
    conn.close()
    return render_template(
        "events.html",
        events=events,
        categories=categories,
        orgs=orgs,
        q=q,
        selected_category=category,
        selected_orgID=orgID,
    )


@app.route("/events/add", methods=["GET", "POST"])
def add_event():
    conn = get_db_connection()
    orgs = conn.execute("SELECT orgID, orgName FROM Organization ORDER BY orgName").fetchall()
    categories = conn.execute("SELECT categoryName FROM EventCategory ORDER BY categoryName").fetchall()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        eventDate = request.form.get("eventDate", "").strip()
        startTime = request.form.get("startTime", "").strip()
        location = request.form.get("location", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        capacity = request.form.get("capacity", "").strip()
        orgID = request.form.get("orgID", "").strip()

        if not title or not eventDate or not orgID:
            flash("Title, date, and organization are required.", "error")
            conn.close()
            return render_template("event_form.html", event=request.form, orgs=orgs, categories=categories, action="Add")

        capacity = int(capacity) if capacity else 0
        conn.execute(
            """
            INSERT INTO Event (title, eventDate, startTime, location, category, description, capacity, orgID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (title, eventDate, startTime, location, category, description, capacity, orgID),
        )
        conn.commit()
        conn.close()
        flash("Event added successfully.", "success")
        return redirect(url_for("events"))

    conn.close()
    return render_template("event_form.html", event=None, orgs=orgs, categories=categories, action="Add")


@app.route("/events/edit/<int:id>", methods=["GET", "POST"])
def edit_event(id):
    conn = get_db_connection()
    event = conn.execute("SELECT * FROM Event WHERE eventID = ?", (id,)).fetchone()
    if event is None:
        conn.close()
        abort(404)
    orgs = conn.execute("SELECT orgID, orgName FROM Organization ORDER BY orgName").fetchall()
    categories = conn.execute("SELECT categoryName FROM EventCategory ORDER BY categoryName").fetchall()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        eventDate = request.form.get("eventDate", "").strip()
        startTime = request.form.get("startTime", "").strip()
        location = request.form.get("location", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        capacity = request.form.get("capacity", "").strip()
        orgID = request.form.get("orgID", "").strip()

        if not title or not eventDate or not orgID:
            flash("Title, date, and organization are required.", "error")
            conn.close()
            return render_template("event_form.html", event=request.form, orgs=orgs, categories=categories, action="Edit")

        capacity = int(capacity) if capacity else 0
        conn.execute(
            """
            UPDATE Event
            SET title = ?, eventDate = ?, startTime = ?, location = ?, category = ?,
                description = ?, capacity = ?, orgID = ?
            WHERE eventID = ?
            """,
            (title, eventDate, startTime, location, category, description, capacity, orgID, id),
        )
        conn.commit()
        conn.close()
        flash("Event updated successfully.", "success")
        return redirect(url_for("events"))

    conn.close()
    return render_template("event_form.html", event=event, orgs=orgs, categories=categories, action="Edit")


@app.route("/events/delete/<int:id>", methods=["POST"])
def delete_event(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM Event WHERE eventID = ?", (id,))
    conn.commit()
    conn.close()
    flash("Event deleted successfully. Related RSVPs were also removed.", "success")
    return redirect(url_for("events"))


@app.route("/events/view/<int:id>")
def view_event(id):
    conn = get_db_connection()
    event = conn.execute(
        """
        SELECT e.*, o.orgName, o.contactEmail,
               COALESCE(r.confirmedCount, 0) AS confirmedCount,
               e.capacity - COALESCE(r.confirmedCount, 0) AS seatsLeft
        FROM Event e
        JOIN Organization o ON e.orgID = o.orgID
        LEFT JOIN (
            SELECT eventID, COUNT(*) AS confirmedCount
            FROM RSVP
            WHERE status = 'Confirmed'
            GROUP BY eventID
        ) r ON e.eventID = r.eventID
        WHERE e.eventID = ?
        """,
        (id,),
    ).fetchone()
    if event is None:
        conn.close()
        abort(404)

    rsvps = conn.execute(
        """
        SELECT r.status, r.rsvpDate, s.firstName, s.lastName, s.BMCCemail
        FROM RSVP r
        JOIN Student s ON r.studentID = s.studentID
        WHERE r.eventID = ?
        ORDER BY s.lastName, s.firstName
        """,
        (id,),
    ).fetchall()
    conn.close()
    return render_template("view_event.html", event=event, rsvps=rsvps)


# -------------------- RSVP CRUD --------------------
@app.route("/rsvps")
def rsvps():
    conn = get_db_connection()
    rsvps = conn.execute(
        """
        SELECT r.rsvpID, r.rsvpDate, r.status,
               s.firstName, s.lastName, s.BMCCemail,
               e.title, e.eventDate,
               o.orgName
        FROM RSVP r
        JOIN Student s ON r.studentID = s.studentID
        JOIN Event e ON r.eventID = e.eventID
        JOIN Organization o ON e.orgID = o.orgID
        ORDER BY e.eventDate, s.lastName, s.firstName
        """
    ).fetchall()
    conn.close()
    return render_template("rsvps.html", rsvps=rsvps)


@app.route("/rsvps/add", methods=["GET", "POST"])
def add_rsvp():
    preselected_event = request.args.get("eventID", "")
    conn = get_db_connection()
    students = conn.execute("SELECT studentID, firstName, lastName, BMCCemail FROM Student ORDER BY lastName, firstName").fetchall()
    events = conn.execute("SELECT eventID, title, eventDate FROM Event ORDER BY eventDate, title").fetchall()

    if request.method == "POST":
        studentID = request.form.get("studentID", "").strip()
        eventID = request.form.get("eventID", "").strip()
        rsvpDate = request.form.get("rsvpDate", "").strip() or date.today().isoformat()
        status = request.form.get("status", "").strip()

        if not studentID or not eventID or not status:
            flash("Student, event, and status are required.", "error")
            conn.close()
            return render_template("rsvp_form.html", rsvp=request.form, students=students, events=events, action="Add", today=date.today().isoformat())

        try:
            conn.execute(
                """
                INSERT INTO RSVP (studentID, eventID, rsvpDate, status)
                VALUES (?, ?, ?, ?)
                """,
                (studentID, eventID, rsvpDate, status),
            )
            conn.commit()
            conn.close()
            flash("RSVP added successfully.", "success")
            return redirect(url_for("rsvps"))
        except sqlite3.IntegrityError:
            flash("This student already has an RSVP for that event. Edit the existing RSVP instead.", "error")

    conn.close()
    return render_template(
        "rsvp_form.html",
        rsvp={"eventID": preselected_event, "rsvpDate": date.today().isoformat()},
        students=students,
        events=events,
        action="Add",
        today=date.today().isoformat(),
    )


@app.route("/rsvps/edit/<int:id>", methods=["GET", "POST"])
def edit_rsvp(id):
    conn = get_db_connection()
    rsvp = conn.execute("SELECT * FROM RSVP WHERE rsvpID = ?", (id,)).fetchone()
    if rsvp is None:
        conn.close()
        abort(404)
    students = conn.execute("SELECT studentID, firstName, lastName, BMCCemail FROM Student ORDER BY lastName, firstName").fetchall()
    events = conn.execute("SELECT eventID, title, eventDate FROM Event ORDER BY eventDate, title").fetchall()

    if request.method == "POST":
        studentID = request.form.get("studentID", "").strip()
        eventID = request.form.get("eventID", "").strip()
        rsvpDate = request.form.get("rsvpDate", "").strip()
        status = request.form.get("status", "").strip()

        if not studentID or not eventID or not rsvpDate or not status:
            flash("All RSVP fields are required.", "error")
            conn.close()
            return render_template("rsvp_form.html", rsvp=request.form, students=students, events=events, action="Edit", today=date.today().isoformat())

        try:
            conn.execute(
                """
                UPDATE RSVP
                SET studentID = ?, eventID = ?, rsvpDate = ?, status = ?
                WHERE rsvpID = ?
                """,
                (studentID, eventID, rsvpDate, status, id),
            )
            conn.commit()
            conn.close()
            flash("RSVP updated successfully.", "success")
            return redirect(url_for("rsvps"))
        except sqlite3.IntegrityError:
            flash("This student already has an RSVP for that event.", "error")

    conn.close()
    return render_template("rsvp_form.html", rsvp=rsvp, students=students, events=events, action="Edit", today=date.today().isoformat())


@app.route("/rsvps/delete/<int:id>", methods=["POST"])
def delete_rsvp(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM RSVP WHERE rsvpID = ?", (id,))
    conn.commit()
    conn.close()
    flash("RSVP deleted successfully.", "success")
    return redirect(url_for("rsvps"))


# -------------------- Reports --------------------
@app.route("/reports")
def reports():
    conn = get_db_connection()

    total_rsvps_per_event = conn.execute(
        """
        SELECT e.title, e.eventDate, o.orgName,
               COUNT(r.rsvpID) AS totalRSVPs,
               SUM(CASE WHEN r.status = 'Confirmed' THEN 1 ELSE 0 END) AS confirmedRSVPs,
               e.capacity,
               e.capacity - SUM(CASE WHEN r.status = 'Confirmed' THEN 1 ELSE 0 END) AS seatsLeft
        FROM Event e
        JOIN Organization o ON e.orgID = o.orgID
        LEFT JOIN RSVP r ON e.eventID = r.eventID
        GROUP BY e.eventID, e.title, e.eventDate, o.orgName, e.capacity
        ORDER BY totalRSVPs DESC, e.eventDate
        """
    ).fetchall()

    events_by_category = conn.execute(
        """
        SELECT category, COUNT(*) AS eventCount
        FROM Event
        GROUP BY category
        ORDER BY eventCount DESC, category
        """
    ).fetchall()

    events_by_org = conn.execute(
        """
        SELECT o.orgName, COUNT(e.eventID) AS eventCount
        FROM Organization o
        LEFT JOIN Event e ON o.orgID = e.orgID
        GROUP BY o.orgID, o.orgName
        HAVING eventCount > 0
        ORDER BY eventCount DESC, o.orgName
        """
    ).fetchall()

    students_multiple_rsvps = conn.execute(
        """
        SELECT s.firstName, s.lastName, s.BMCCemail, COUNT(r.rsvpID) AS rsvpCount
        FROM Student s
        JOIN RSVP r ON s.studentID = r.studentID
        GROUP BY s.studentID, s.firstName, s.lastName, s.BMCCemail
        HAVING COUNT(r.rsvpID) >= 2
        ORDER BY rsvpCount DESC, s.lastName
        """
    ).fetchall()

    conn.close()
    return render_template(
        "reports.html",
        total_rsvps_per_event=total_rsvps_per_event,
        events_by_category=events_by_category,
        events_by_org=events_by_org,
        students_multiple_rsvps=students_multiple_rsvps,
    )
if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)