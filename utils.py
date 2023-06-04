import sqlite3
from datetime import datetime, timedelta


def patch_attendance(userid):
    db = sqlite3.connect("./attendance.sqlite", isolation_level=None)
    cursor = db.cursor()
    attendanceforweek, fullattendance, streak, registered = getattendance(userid)
    if fullattendance == 100:
        return {"updated": "None"}
    week, day = get_day()
    weeks = []
    for x in range(week):
        weeks.append(x + 1)
    weeks.reverse()
    for x in weeks:
        if x == week:
            days = []
            for y in range(day):
                days.append(y + 1)
            days.reverse()
            for y in days:
                cursor.execute(
                    f"""
                SELECT DISTINCT present
                FROM week{x}day{y}
                WHERE userid = "{userid}"
                """
                )
                present = cursor.fetchone()
                if present is None:
                    cursor.execute(
                        f"""
                    INSERT INTO week{x}day{y} (userid, present)
                    VALUES ("{userid}", 1);
                    """
                    )
                    return {"updated": f"week{x}day{y}"}
        else:
            days = []
            for y in range(7):
                days.append(y + 1)
            days.reverse()
            for y in days:
                cursor.execute(
                    f"""
                SELECT DISTINCT present
                FROM week{x}day{y}
                WHERE userid = "{userid}"
                """
                )
                present = cursor.fetchone()
                if present is None:
                    cursor.execute(
                        f"""
                    INSERT INTO week{x}day{y} (userid, present)
                    VALUES ("{userid}", 1);
                    """
                    )
                    return {"updated": f"week{x}day{y}"}


def get_day():
    db = sqlite3.connect("./attendance.sqlite", isolation_level=None)
    cursor = db.cursor()
    cursor.execute(
        f"""
        SELECT name FROM sqlite_master 
        WHERE type IN ('table','view') 
        AND name NOT LIKE 'sqlite_%'
    """
    )
    tables = cursor.fetchall()
    days = len(tables) - 1
    day = days % 7
    if day == 0:
        day = 7
    week = ((days - day) / 7) + 1

    return int(week), day


def get_members_10_streak():
    allmembers = get_members()
    members = []
    for member in allmembers:
        attendanceforweek, fullattendance, streak, registered = getattendance(member)
        if streak % 10 == 0 and streak != 0:
            members.append(member)
    return {"status": "OK", "members": members}


def get_members():
    db = sqlite3.connect("attendance.sqlite", isolation_level=None)
    cursor = db.cursor()
    cursor.execute(
        """
    SELECT userid
    FROM members
    """
    )
    membersfromdb = cursor.fetchall()
    members = []
    for member in membersfromdb:
        members.append(member[0])
    return members


def get_members_above(type, cutoff):
    allmembers = get_members()
    members = []
    if type == "week":
        for member in allmembers:
            attendanceforweek, fullattendance, streak, registered = getattendance(
                member
            )
            if attendanceforweek >= cutoff:
                members.append(member)
        return {"status": "OK", "members": members}
    elif type == "full":
        for member in allmembers:
            attendanceforweek, fullattendance, streak, registered = getattendance(
                member
            )
            if fullattendance >= cutoff:
                members.append(member)
        return {"status": "OK", "members": members}


def get_all():
    members = get_members()
    return {"status": "OK", "members": members}


def get_present():
    week, day = get_day()
    db = sqlite3.connect("attendance.sqlite", isolation_level=None)
    cursor = db.cursor()
    cursor.execute(
        f"""
        SELECT userid
        FROM week{week}day{day}
        WHERE present = 1
    """
    )
    presentfromdb = cursor.fetchall()
    present = []
    for x in presentfromdb:
        present.append(x[0])
    return {"status": "OK", "userid": present}


def getattendance(user_id):
    week, day = get_day()
    userid = user_id
    dayspresent = 0
    db = sqlite3.connect("./attendance.sqlite", isolation_level=None)
    cursor = db.cursor()
    cursor.execute(
        f"""
        SELECT DISTINCT dayjoined
        FROM members
        WHERE userid = "{userid}"
    """
    )
    dayjoined = cursor.fetchone()
    if dayjoined is not None:
        dayjoinedf = datetime.strptime(dayjoined[0], "%d/%m/%y")
        currentday = datetime.utcnow() + timedelta(hours=+8)
        sincejoined = currentday - dayjoinedf

        for x in range(day):
            cursor.execute(
                f"""
                SELECT DISTINCT present
                FROM week{week}day{x+1}
                WHERE userid = "{userid}"
            """
            )

            present = cursor.fetchone()
            if present is not None:
                dayspresent = dayspresent + 1
        attendanceforweek = (dayspresent / day) * 100

        dayspresent = 0
        for y in range(week):
            if y + 1 != week:
                for z in range(7):
                    cursor.execute(
                        f"""
                        SELECT DISTINCT present
                        FROM week{y+1}day{z+1}
                        WHERE userid = "{userid}"
                    """
                    )
                    present = cursor.fetchone()
                    if present is not None:
                        dayspresent = dayspresent + 1
            elif y + 1 == week:
                for z in range(day):
                    cursor.execute(
                        f"""
                        SELECT DISTINCT present
                        FROM week{y+1}day{z+1}
                        WHERE userid = "{userid}"
                    """
                    )
                    present = cursor.fetchone()
                    if present is not None:
                        dayspresent = dayspresent + 1
        fullattendance = (dayspresent / (sincejoined.days + 1)) * 100
        streak = 0
        for y in range(week):
            if y + 1 != week:
                for z in range(7):
                    cursor.execute(
                        f"""
                        SELECT DISTINCT present
                        FROM week{y+1}day{z+1}
                        WHERE userid = "{userid}"
                    """
                    )
                    present = cursor.fetchone()
                    if present is not None:
                        streak = streak + 1
                    if present is None:
                        streak = 0
            elif y + 1 == week:
                for z in range(day):
                    cursor.execute(
                        f"""
                        SELECT DISTINCT present
                        FROM week{y+1}day{z+1}
                        WHERE userid = "{userid}"
                    """
                    )
                    present = cursor.fetchone()
                    if present is not None:
                        streak = streak + 1
                    if present is None:
                        streak = 0
        registered = True
        return attendanceforweek, fullattendance, streak, registered

    else:
        registered = False
        return 0, 0, 0, registered


def getrep(userid):
    db = sqlite3.connect("./points.sqlite", isolation_level=None)
    cursor = db.cursor()
    cursor.execute(
        f"""
                SELECT points
                FROM bank
                WHERE userid = "{userid}"
            """
    )
    points = cursor.fetchone()
    if points is None:
        return 0
    else:
        return round(float(points[0]), 1)


def mark_present(userid):
    week, day = get_day()
    db = sqlite3.connect("./attendance.sqlite", isolation_level=None)
    cursor = db.cursor()

    cursor.execute(
        f"""
        SELECT DISTINCT dayjoined
        FROM members
        WHERE userid = "{userid}"
    """
    )
    joined = cursor.fetchone()
    currentdate = datetime.utcnow() + timedelta(hours=+8)
    currentdate = currentdate.strftime("%d/%m/%y")
    if joined is None:
        cursor.execute(
            f"""
        INSERT INTO members (userid, dayjoined)
        VALUES ("{userid}", "{currentdate}");
        """
        )

    cursor.execute(
        f"""
        SELECT DISTINCT present
        FROM week{week}day{day}
        WHERE userid = "{userid}"
    """
    )
    present = cursor.fetchone()
    if present is None:
        cursor.execute(
            f"""
        INSERT INTO week{week}day{day} (userid, present)
        VALUES ("{userid}", 1);
        """
        )
        return {"status": "OK", "first": True}
    else:
        return {"status": "OK", "first": False}


def get_points_leaderboard():
    db = sqlite3.connect("points.sqlite", isolation_level=None)
    cursor = db.cursor()
    cursor.execute(
        f"""
        SELECT points
        FROM bank;
    """
    )
    points = cursor.fetchall()
    fpoints = []
    for point in points:
        fpoints.append(round(point[0], 1))
    cursor.execute(
        f"""
        SELECT userid
        FROM bank;
    """
    )
    users = cursor.fetchall()
    fusers = []
    for x in range(len(users)):
        fusers.append(int(users[x][0]))
    zipped = zip(fpoints, fusers)
    fusers = [x for _, x in sorted(zipped)]
    fusers.reverse()
    fpoints.sort(reverse=True)
    if len(fusers) < 10:
        return {"status": "OK", "userid": fusers, "reps": fpoints}
    else:
        top10user = []
        top10point = []
        for x in range(10):
            top10user.append(fusers[x])
            top10point.append(fpoints[x])
        return {"status": "OK", "userid": top10user, "reps": top10point}


def get_attendance_leaderboard():
    db = sqlite3.connect("./attendance.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""
        SELECT userid
        FROM members
    """
    )
    usersfromdb = cursor.fetchall()
    users = []
    for user in usersfromdb:
        users.append(user[0])
    streaks = []
    for user in users:
        attendanceforweek, fullattendance, streak, registered = getattendance(user)
        streaks.append(streak)
    zipped = zip(streaks, users)
    usersorted = [x for _, x in sorted(zipped)]
    usersorted.reverse()
    streaksorted = streaks
    streaksorted.sort(reverse=True)
    if len(usersorted) < 10:
        return {"status": "OK", "userid": usersorted, "streaks": streaksorted}
    else:
        top10user = []
        top10streak = []
        for x in range(10):
            top10user.append(usersorted[x])
            top10streak.append(streaksorted[x])
        return {"status": "OK", "userid": top10user, "streaks": top10streak}


def create_newday():
    db = sqlite3.connect("./attendance.sqlite")
    cursor = db.cursor()
    week, day = get_day()
    day += 1
    if day == 8:
        week += 1
        day = 1
    cursor.execute(
        f"""
            CREATE TABLE IF NOT EXISTS week{week}day{day}
            (
                userid TEXT, 
                present INTEGER
            )
        """
    )
    return {
        "status": "OK",
        "table created": f"week{week}day{day}",
        "week": week,
        "day": day,
    }


def add_points(userid, points):
    db = sqlite3.connect("./points.sqlite", isolation_level=None)
    cursor = db.cursor()
    cursor.execute(
        f"""
            SELECT points
            FROM bank
            WHERE userid = "{userid}"
        """
    )
    pointsfromdb = cursor.fetchone()
    if pointsfromdb is None:
        cursor.execute(
            f"""
            INSERT INTO bank (userid, points)
            VALUES ("{userid}", {float(points)});
            """
        )
        return {"status": "OK", "before": 0, "after": round(points, 1)}
    else:
        cursor.execute(
            f"""
            UPDATE bank
            SET points = points + {float(points)}
            WHERE userid = "{userid}";
            """
        )
        return {
            "status": "OK",
            "before": round(pointsfromdb[0], 1),
            "after": round(pointsfromdb[0] + points, 1),
        }


def minus_points(userid, points):
    db = sqlite3.connect("./points.sqlite", isolation_level=None)
    cursor = db.cursor()
    cursor.execute(
        f"""
            SELECT points
            FROM bank
            WHERE userid = "{userid}"
        """
    )
    pointsfromdb = cursor.fetchone()
    if pointsfromdb is None:
        cursor.execute(
            f"""
            INSERT INTO bank (userid, points)
            VALUES ("{userid}", {float(points)});
            """
        )
        return {"status": "OK", "before": 0, "after": round(points, 1)}
    else:
        cursor.execute(
            f"""
            UPDATE bank
            SET points = points - {float(points)}
            WHERE userid = "{userid}";
            """
        )
        return {
            "status": "OK",
            "before": round(pointsfromdb[0], 1),
            "after": round(pointsfromdb[0] - points, 1),
        }
