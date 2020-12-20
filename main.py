import sqlite3 as sql
import datetime
import smtplib
from pathlib import Path
from email.message import EmailMessage

mydb = sql.connect("data.db")
cursor = mydb.cursor()


def sendmail(id, passwd) -> None:
    today = str(datetime.datetime.now().strftime("%d/%m/%y"))
    report = Path("report.html").read_text()

    mail = EmailMessage()
    mail["from"] = id
    mail["to"] = id
    mail["subject"] = f"Hey, Abhishek your performance report till {today}!!!"
    mail.set_content(report, "html")

    try:
        with smtplib.SMTP("SMTP.gmail.com", 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(id, passwd)
            s.send_message(mail)
    except Exception as e:
        print("%s: %s" % (e.__class__.__name__, e))


def points_gen(target, days, marks, totalmarks, totalpoints) -> dict:
    marks = (marks/totalmarks)*100
    days = (days/6)*100
    target = (target/12)*100
    points = {
        "points_get": (marks + days + target)/2,
        "total_points": totalpoints
        }
    return points


if __name__ == "__main__":
    try:
        cursor.execute("""CREATE TABLE alix (
            `date` text,
            `points` text,
            `target` text,
            `days` text
        )""")
    except Exception:
        pass

    print(5000*"\n")
    print(""""
    Hey, Abhishek plz provide details of your work done in this week.
    """)

    target = input("How many targets have you completed in this week? ")
    days = input("How many days have you study in this week? ")
    marks = input("How many marks have you got in weekly test?")

    today = str(datetime.datetime.now().strftime("%d/%m/%y"))
