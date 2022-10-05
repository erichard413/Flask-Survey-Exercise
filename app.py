from http.client import BAD_REQUEST
from flask import Flask, request, render_template, redirect, session, flash
from surveys import *

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"




# When the user submits an answer, you should append this answer to your responses list, and then redirect them to the next question.

# The Flask Debug Toolbar will be very useful in looking at the submitted form data.

responses = {}
# survey_name = "satisfaction" ## name of survey dynamically creates Q pages for survey - need to implement UI to change this on page.
# title = surveys[survey_name].title
# survey = surveys[survey_name]
survey_names = surveys.keys()
@app.route("/")
def go_home():
    """Goes home"""
    return redirect("/home")

@app.route("/startnew")
def start_survey():
    """home page to start the survey. / is routed to start.html"""
    name = request.args["name"]
    title = surveys[name].title
    instr = surveys[name].instructions
    return render_template("start.html", title = title, instr = instr, name = name)

@app.route("/questions/<index>", methods = ["POST", "GET"])
def question_id(index):
    """dynamic routing for our questions, each question is displayed on a page
        try/catch to filter out invalid out of range URLs
    """
    if (request.args["name"]) in responses.keys():
        return render_template("end.html")
    # if responses[request.args["name"]]:
    #     return render_template("end.html")
    try:
        s_name = (request.args["name"])
        session["s_name"] = s_name
        title = surveys[s_name].title
        survey = surveys[s_name]
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
            return redirect("/home")
    except KeyError:
            session.pop('index', None)
            stored_responses = session["responses"]
            stored_responses.clear()
            session["responses"] = stored_responses
            flash("You do not have permission to access that page!", "error")
            return redirect("/home")

@app.route("/answer", methods=["POST"])
def answered_question():
    """store response from prev question to responses var, then forward to next question"""
    s_name = session["s_name"]
    try:
        comment = request.form["comment"]
        options = request.form["options"]
        answer = {options : comment}
    except:
        answer = request.form["options"]
    save_responses = session["responses"]
    save_responses.append(answer)
    session["responses"] = save_responses
    next_idx = int(session.get('index', None)) + 1
    if next_idx < len(surveys[s_name].questions):
        return redirect(f"/questions/{next_idx}?name={s_name}")
    else:
        
        survey = surveys[s_name]
        questions = survey.questions
        output = []
        for i in range(len(questions)):
            if type(save_responses[i]) is dict:
                for k in save_responses[i]:
                    val = save_responses[i][k]
                    line = f"{questions[i].question} - {k}: {val}"
            else:
                line = f"{str(questions[i].question)} - {str(save_responses[i])}" 
            output.append(line)
        responses[s_name] = (save_responses)
        flash("Form submitted successfully!", "success")   
        return render_template("end.html", output = output)

@app.route("/home")
def select_survey():
    """User should select survey, survey name is retrieved"""
    surveys = survey_names
    return render_template("home.html", surveys = surveys)

@app.route("/home", methods=["POST"])
def start_new():
    """User initiates a new individual "session" to store answers"""
    session["responses"] = []
    s_name = (request.form["s_name"])
    return redirect(f"/startnew?name={s_name}")


