from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



# When the user submits an answer, you should append this answer to your responses list, and then redirect them to the next question.

# The Flask Debug Toolbar will be very useful in looking at the submitted form data.

responses = []
survey_name = "satisfaction" ## name of survey dynamically creates Q pages for survey - need to implement UI to change this on page.
title = surveys[survey_name].title
survey = surveys[survey_name]
survey_names = surveys.keys()
@app.route("/index.html")
def initialize_page():
    return redirect("/")

@app.route("/")
def start_survey():
    """home page to start the survey. / is routed to start.html"""
    instr = survey.instructions
    return render_template("start.html", title=title, instr = instr)

# @app.route("/home")
# def select_survey():
#     """User should select survey, survey name is retrieved"""
#     surveys = survey_names
#     return render_template("home.html", surveys = surveys)

@app.route("/questions/<index>")
def question_id(index):
    """dynamic routing for our questions, each question is displayed on a page
        try/catch to filter out invalid out of range URLs
    """
    if responses:
        return render_template("end.html")
    try:
        questions_list = getattr(survey, "questions")
        question_obj = questions_list[int(index)]
        num_of_responses = len(session["responses"])
        txt = question_obj.allow_text
        choices = question_obj.choices
        question = question_obj.question
        idx = index
        session['index'] = idx
        if int(index) == num_of_responses:
            return render_template("questions.html", title=title, question=question, choices = choices, txt = txt)
        else:
            session.pop('index', None)
            flash("You do not have permission to access that page!", "error")
            return redirect("/")
    except IndexError:
            session.pop('index', None)
            stored_responses = session["responses"]
            stored_responses.clear()
            session["responses"] = stored_responses
            flash("You do not have permission to access that page!", "error")
            return redirect("/startnew")


@app.route("/answer", methods=["POST"])
def answered_question():
    """store response from prev question to responses var, then forward to next question"""
    answer = request.form["options"]
    save_responses = session["responses"]
    save_responses.append(answer)
    session["responses"] = save_responses
    next_idx = int(session.get('index', None)) + 1
    if next_idx < len(survey.questions):
        return redirect(f"/questions/{next_idx}")
    else:
        responses.append(save_responses)
        flash("Form submitted successfully!", "success")     
        return render_template("end.html")

@app.route("/startnew", methods=["GET", "POST"])
def start_new():
    """User initiates a new individual "session" to store answers"""
    session["responses"] = []
    return redirect("/questions/0")


