"""RA7: Binomial Theorem / Pascal's Triangle formative feedback.

Imported by math_interactive.math131.__init__.
Authoritative grades are assigned by nbgrader, not this module.
"""
import os
import math
from html import escape
from IPython.display import display, HTML

QUESTION_FEEDBACK = {'q7': {'answer': 'B', 'feedback': {'A': 'That is row 4, not row 5.', 'C': 'Check the two middle entries when building row 5.', 'D': 'That list belongs to the next row.'}, 'hint': "The coefficients of (a+b)^n come from row n of Pascal's Triangle. Build row 5 from row 4 by adding adjacent entries and placing 1 at both ends."}, 'q8': {'answer': 'C', 'feedback': {'A': 'Check the factorial simplification carefully.', 'B': 'Remember to divide by both 3! and 4!.', 'D': 'The binomial coefficient is not simply n.'}, 'hint': 'Use n choose k = n!/[k!(n-k)!]. For 7 choose 3, simplify 7!/(3!4!).'}, 'q9': {'answer': 'A', 'feedback': {'B': 'The middle terms do not disappear in a binomial expansion.', 'C': "Check the middle coefficient in row 4 of Pascal's Triangle.", 'D': 'The x³ and x terms are also part of the expansion.'}, 'hint': "Use row 4 of Pascal's Triangle: 1, 4, 6, 4, 1. Pair those coefficients with descending powers of x and ascending powers of 1."}, 'q10': {'answer': 'D', 'feedback': {'A': '6 is the binomial coefficient, but you must also include 3².', 'B': 'Check the power of 3 associated with the x² term.', 'C': 'Include the binomial coefficient C(4,2).'}, 'hint': 'The x² term corresponds to k=2 in (x+3)^4. Compute C(4,2)·x²·3² and identify the numerical coefficient.'}, 'q11': {'answer': 'B', 'feedback': {'A': 'This is the expansion of (x+1)^3; account for the negative term.', 'C': 'Because (-1)² is positive, the x term should be positive.', 'D': 'Check the signs of the x² and x terms.'}, 'hint': 'Write (x-1)^3 as (x+(-1))^3. Track the powers of -1: -1, +1, -1.'}, 'q12': {'answer': 'C', 'feedback': {'A': 'You used the binomial coefficient but omitted the factor 3².', 'B': 'Check the power of 3 in the third term.', 'D': 'For the third term, the power of x should be 5-2=3.'}, 'hint': 'The 3rd term corresponds to k=2. Use C(5,2)x^(5-2)3².'}, 'q13': {'answer': 'A', 'feedback': {'B': '36 is 6², but row sums follow powers of 2.', 'C': 'Use the row-sum identity 2^n.', 'D': 'Use the row-sum identity 2^n.'}, 'hint': "The sum of the entries in row n of Pascal's Triangle is 2^n. Here n=6."}}

def _feedback(message, color):
    display(HTML(
        f'<div style="padding:10px 12px;margin:6px 0;'
        f'border-left:4px solid {color};border-radius:4px;">{message}</div>'
    ))

def _grading():
    return os.environ.get("NBGRADER_EXECUTION", "").lower() in {"autograde", "validate"}

def check_answer(question_id, student_answer):
    """Provide immediate feedback for an RA7 multiple-choice answer."""
    if _grading():
        return None
    if question_id not in QUESTION_FEEDBACK:
        raise ValueError(f"Unknown RA7 question ID: {question_id}")
    answer = "" if student_answer is None else str(student_answer).strip().upper()
    if answer not in {"A", "B", "C", "D"}:
        _feedback("Enter A, B, C, or D inside the quotation marks, then rerun this cell.", "#ad8200")
        return None
    cfg = QUESTION_FEEDBACK[question_id]
    if answer == cfg["answer"]:
        _feedback("✅ <strong>Correct — good job!</strong>", "#2e7d32")
    else:
        reason = cfg["feedback"].get(answer, "Review the question and try again.")
        _feedback(
            "❌ <strong>Not quite. Try again.</strong> "
            + escape(reason) + "<br><small><strong>Hint:</strong> "
            + escape(cfg["hint"]) + "</small>", "#c62828"
        )
    return None

def check_code_answer(question_id, function):
    """Provide formative feedback for RA7's Pascal row coding task."""
    if _grading():
        return None
    if question_id != "q14":
        raise ValueError(f"Unknown RA7 code question ID: {question_id}")
    if not callable(function):
        _feedback("Keep the function named pascal_row(n).", "#ad8200")
        return None
    try:
        results = [function(n) for n in (0, 2, 4, 6)]
        expected = [[math.comb(n, k) for k in range(n+1)] for n in (0, 2, 4, 6)]
        correct = all(isinstance(got, list) and got == want for got, want in zip(results, expected))
    except Exception as exc:
        _feedback("❌ Your function raised an error: " + escape(str(exc))
                  + "<br><small>Hint: return a list of binomial coefficients.</small>", "#c62828")
        return None
    if correct:
        _feedback("✅ <strong>Correct — your Pascal rows passed the practice checks!</strong>", "#2e7d32")
    else:
        _feedback("❌ Not quite. Return a list with n+1 entries; try math.comb(n, k) for k from 0 through n.", "#c62828")
    return None
