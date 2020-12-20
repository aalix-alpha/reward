import sqlite3 as sql
import datetime
import smtplib
from pathlib import Path
from email.message import EmailMessage

mydb = sql.connect("data.db")
cursor = mydb.cursor()


def sendmail() -> None:
    id = "abhishekmalhotra2914@gmail.com"
    passwd = "aalix19@Abhi"

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
        "points_get": ((marks + days + target)/5)/2,
        "total_points": totalpoints + ((marks + days + target)/5)/2
        }
    return points


def mail_it():
    report = """
<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        * {
            font-style: italic;
            font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
        }
        
        .moderate {
            color: rgb(205, 240, 11);
        }
        
        .better {
            color: rgb(14, 224, 119);
        }
        
        .worst {
            color: red;
        }
        
        #intro {
            font-family: comic sans-serif;
        }
    </style>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

    <title>Performance</title>
</head>

<body>
    <p id="intro">Hey, Abhishek your performance report of this week is as follow:<br><br></p>
    <table class="table">
        <thead>
            <tr>
                <th scope="col"><b>Date  </b></th>
                <th scope="col"><b> Targets Completed</b></th>
                <th scope="col"><b> No. of days study</b></th>
                <th scope="col"><b> Test Marks</b></th>
                <th scope="col"><b> Points</b></th>
            </tr>
        </thead>
        <tbody>
"""

    for record in cursor.execute("SELECT * FROM alix WHERE 1").fetchall():
        if (int(record[1].split(".")[0])/2)*100 >= 85:
            report += f"""
            <tr class= "better">
                <td scope="row">{record[0]}</td>
                <td>{record[2]}</td>
                <td>{record[4]}</td>
                <td>{record[3]}</td>
                <td>{int(record[1].split(".")[0])/2}</td>
            </tr>
        </tbody>
    </table>

    <p class="better" id="result">Abhishek your performance is seem to be better than last week.</p>

    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js" integrity="sha384-q2kxQ16AaE6UbzuKqyBE9/u/KzioAlnx2maXQHiDX9d4/zp8Ok3f+M7DPm+Ib6IU" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.min.js" integrity="sha384-pQQkAEnwaBkjpqZ8RU1fF1AKtTcHJwFl3pblpTlHXybJjHpMYo79HY3hIi4NKxyj" crossorigin="anonymous"></script>
</body>

</html>
"""

        elif (int(record[1].split(".")[0])/2)*100 >= 65:
            report += f"""
            <tr class= "moderate">
                <td scope="row">{record[0]}</td>
                <td>{record[2]}</td>
                <td>{record[4]}</td>
                <td>{record[3]}</td>
                <td>{int(record[1].split(".")[0])/2}</td>
            </tr>
        </tbody>
    </table>

    <p class="moderate" id="result">Abhishek your performance is seem to be moderate as compare to last week.</p>

    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js" integrity="sha384-q2kxQ16AaE6UbzuKqyBE9/u/KzioAlnx2maXQHiDX9d4/zp8Ok3f+M7DPm+Ib6IU" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.min.js" integrity="sha384-pQQkAEnwaBkjpqZ8RU1fF1AKtTcHJwFl3pblpTlHXybJjHpMYo79HY3hIi4NKxyj" crossorigin="anonymous"></script>
</body>

</html>
"""

        else:
            report += f"""
            <tr class= "worst">
                <td scope="row">{record[0]}</td>
                <td>{record[2]}</td>
                <td>{record[4]}</td>
                <td>{record[3]}</td>
                <td>{int(record[1].split(".")[0])/2}</td>
            </tr>
        </tbody>
    </table>

    <p class="worst" id="result">Abhishek your performance is seem to be worst than last week.</p>

    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js" integrity="sha384-q2kxQ16AaE6UbzuKqyBE9/u/KzioAlnx2maXQHiDX9d4/zp8Ok3f+M7DPm+Ib6IU" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.min.js" integrity="sha384-pQQkAEnwaBkjpqZ8RU1fF1AKtTcHJwFl3pblpTlHXybJjHpMYo79HY3hIi4NKxyj" crossorigin="anonymous"></script>
</body>

</html>
"""

    with open("report.html", "w") as f:
        f.write(report)

    sendmail()



if __name__ == "__main__":
    try:
        cursor.execute("""CREATE TABLE alix (
            `date` text,
            `points` text,
            `target` text,
            `marks` text,
            `days` text
        )""")
    except Exception as e:
        print("%s: %s" % (e.__class__.__name__, e))

    # print(5000*"\n")
    print("""
    Hey, Abhishek plz provide details of your work done in this week.
    """)

    target = input("How many targets have you completed in this week? ")
    days = input("How many days have you study in this week? ")
    marks = input("How many marks have you got in weekly test? ")

    today = str(datetime.datetime.now().strftime("%d/%m/%y"))

    points = 0
    for record in cursor.execute("SELECT * FROM alix WHERE 1").fetchall():
        points += float(record[1])

    cursor.execute("""
        INSERT INTO alix(
            date,
            points,
            target,
            marks,
            days
        )
        Values(
            ?,
            ?,
            ?,
            ?,
            ?
        )""",
        [
            today,
            points_gen(
                int(target),
                int(days),
                float(marks.split("/")[0]),
                float(marks.split("/")[1]),
                float(points)
                )["points_get"],
            target,
            marks,
            days
        ]
    )

    mydb.commit()
    mail_it()
