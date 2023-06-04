from fastapi import FastAPI
from utils import *

app = FastAPI()


@app.get("/api/userdata/{userid}")
def get_userdata(userid: int):
    attendanceforweek, fullattendance, streak, registered = getattendance(userid)
    rep = getrep(userid)
    if registered:
        user = {
            "weekly_attendance": int(attendanceforweek),
            "full_attendance": int(fullattendance),
            "streak": streak,
            "reps": rep,
        }
    else:
        user = {"weekly_attendance": 0, "full_attendance": 0, "streak": 0, "reps": rep}
    return user


@app.put("/api/medical_leave/{userid}/{days}")
def medicial_leave(userid: int, days: int):
    response = []
    for x in range(days):
        response.append(patch_attendance(userid)["updated"])

    return {"status": "OK", "userid": f"{userid}", "updated": response}


@app.get("/api/attendance_leaderboard")
def attendance_leaderboard():
    response = get_attendance_leaderboard()
    return response


@app.get("/api/get_10_streak")
def get10streak():
    response = get_members_10_streak()
    return response


@app.get("/api/reps_leaderboard")
def reps_leaderboard():
    response = get_points_leaderboard()
    return response


@app.get("/api/present_today")
def present_today():
    response = get_present()
    return response


@app.get("/api/allmembers")
def allmembers():
    response = get_all()
    return response


@app.get("/api/get_members_above/week/{cutoff}")
def get_members_above_week(cutoff: float):
    response = get_members_above("week", cutoff)
    return response


@app.get("/api/get_members_above/full/{cutoff}")
def get_members_above_full(cutoff: float):
    response = get_members_above("full", cutoff)
    return response


@app.get("/api/getday")
def getday():
    week, day = get_day()
    return {"status": "OK", "week": week, "day": day}


@app.post("/api/newday")
def newday():
    response = create_newday()
    return response


@app.put("/api/present/{userid}")
def present(userid: int):
    response = mark_present(userid)
    return response


@app.put("/api/addrep/{userid}/{rep}")
def addrep(userid: int, rep: float):
    response = add_points(userid, rep)
    return response


@app.put("/api/minusrep/{userid}/{rep}")
def minusrep(userid: int, rep: float):
    response = minus_points(userid, rep)
    return response
