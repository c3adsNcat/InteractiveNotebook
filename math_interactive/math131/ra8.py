"""Interactive feedback for MATH 131 RA8. Instructor-maintained package module.

Do not put this module's answer key inside the distributed notebook.
"""
from IPython.display import HTML, display
from html import escape

_QUESTIONS = {
    "q1": ("B", "Net change is signed area: add the positive area and subtract the negative area.", "Recheck which portions lie below the time axis."),
    "q2": ("C", "Combine the given intervals, then reverse the limits to change the sign.", "Reversing integral limits negates the integral."),
    "q3": (39, "Find an antiderivative F and evaluate F(3) - F(0).", "Apply the Fundamental Theorem of Calculus carefully at both bounds."),
    "q4": ("D", "For G(x) = integral from a to x of f(t) dt, G'(x) = f(x).", "Substitute x = 2 into the integrand."),
    "q5": ("A", "Let u = x² + 1, so du = 2x dx; integrate u⁵.", "Remember the power rule and the constant of integration."),
}

def check_answer(question_id, student_answer):
    if question_id not in _QUESTIONS:
        raise ValueError("Unknown RA8 question ID")
    expected, hint, retry = _QUESTIONS[question_id]
    if student_answer is None or (isinstance(student_answer, str) and not student_answer.strip()):
        message, color = "Enter your answer above, then rerun this cell to check it.", "#986400"
    elif isinstance(expected, str):
        if not isinstance(student_answer, str) or student_answer.strip().upper() not in ("A", "B", "C", "D"):
            message, color = "Please enter A, B, C, or D inside quotation marks.", "#986400"
        elif student_answer.strip().upper() == expected:
            message, color = "Correct! Your answer is ready for grading.", "#18794e"
        else:
            message, color = "Not quite. Hint: " + hint + " " + retry + " Update your answer and rerun this cell to try again.", "#b42318"
    elif isinstance(student_answer, (int, float)) and not isinstance(student_answer, bool) and abs(student_answer - expected) < 1e-6:
        message, color = "Correct! Your answer is ready for grading.", "#18794e"
    else:
        message, color = "Not quite. Hint: " + hint + " " + retry + " Update your answer and rerun this cell to try again.", "#b42318"
    display(HTML(f'<div style="border-left:4px solid {color};padding:10px;background:#f8f9fa;color:#222">{escape(message)}</div>'))
