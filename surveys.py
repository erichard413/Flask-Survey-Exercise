# Step One: Surveys
# We’ve provided a file, surveys.py, which includes classes for Question (a single question on a survey, with a question, a list of choices, and whether or not that question should allow for comments) and Survey (a survey, which has a title, instructions, and a list of Question objects).

# For the main part of this exercise, you’ll only need to worry about the satisfaction_survey survey in that file. It does not include any questions that allow comments, so you can skip that for now. (Ignore the personality quiz and the surveys object; those come into play only in the Further Study).

# Play with the satisfaction_survey in ipython to get a feel for how it works: it is an instance of the Survey class, and its .questions attribute is a list of instances of the Question class. You’ll need to understand this structure well, so don’t move on until you feel comfortable with it.




class Question:
    """Question on a questionnaire."""

    def __init__(self, question, choices=None, allow_text=False):
        """Create question (assume Yes/No for choices."""

        if not choices:
            choices = ["Yes", "No"]

        self.question = question
        self.choices = choices
        self.allow_text = allow_text


class Survey:
    """Questionnaire."""

    def __init__(self, title, instructions, questions):
        """Create questionnaire."""

        self.title = title
        self.instructions = instructions
        self.questions = questions


satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])

personality_quiz = Survey(
    "Rithm Personality Test",
    "Learn more about yourself with our personality quiz!",
    [
        Question("Do you ever dream about code?"),
        Question("Do you ever have nightmares about code?"),
        Question("Do you prefer porcupines or hedgehogs?",
                 ["Porcupines", "Hedgehogs"]),
        Question("Which is the worst function name, and why?",
                 ["do_stuff()", "run_me()", "wtf()"],
                 allow_text=True),
    ]
)

surveys = {
    "satisfaction": satisfaction_survey,
    "personality": personality_quiz,
}