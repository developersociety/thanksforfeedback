import base64
import datetime
import json
import os

import gspread
from flask import redirect, render_template, request, url_for
from oauth2client.service_account import ServiceAccountCredentials

from . import app

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    json.loads(base64.b64decode(os.environ["GOOGLE_SERVICE_CREDENTIALS"])), scope
)
client = gspread.authorize(credentials)
sheet = client.open("DLCA Feedback").sheet1


def log_interaction(data):
    timestamp = datetime.datetime.now().isoformat()
    data["timestamp"] = timestamp
    # Append row to Google Sheets
    row = [
        data.get("timestamp"),
        data.get("page"),
        data.get("site_id", ""),
        data.get("question", ""),
        data.get("radio_value", ""),
        data.get("feedback", ""),
    ]
    sheet.append_row(row)


@app.route("/", methods=["GET", "POST"])
def page1():
    site_id = request.args.get("site_id", "default_site_id")
    question = request.args.get("question", "default_question")
    if request.method == "POST":
        site_id = request.form.get("site_id")
        question = request.form.get("question")
        radio_value = request.form.get("radio_value")
        log_interaction(
            {"page": "page1", "site_id": site_id, "question": question, "radio_value": radio_value}
        )
        return redirect(
            url_for("page2", site_id=site_id, question=question, radio_value=radio_value)
        )
    return render_template("page1.html", site_id=site_id, question=question)


@app.route("/page2", methods=["GET", "POST"])
def page2():
    site_id = request.args.get("site_id")
    question = request.args.get("question")
    radio_value = request.args.get("radio_value")
    if request.method == "POST":
        feedback = request.form.get("feedback")
        log_interaction(
            {
                "page": "page2",
                "site_id": site_id,
                "question": question,
                "radio_value": radio_value,
                "feedback": feedback,
            }
        )
        return redirect(url_for("thank_you"))
    return render_template(
        "page2.html", site_id=site_id, question=question, radio_value=radio_value
    )


@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")


if __name__ == "__main__":
    app.run(debug=True)
