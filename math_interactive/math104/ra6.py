"""RA6: Binomial Theorem / Pascal's Triangle formative feedback.

Imported by math_interactive.math104.__init__.
Authoritative grades are assigned by nbgrader, not this module.
"""
from __future__ import annotations

import math
import os
from html import escape
from IPython.display import display, HTML


QUESTION_FEEDBACK = {'q7': {'answer': 'B',
        'feedback': {'A': 'That is row 4, not row 5.',
                     'C': 'Check the two middle entries when building row 5.',
                     'D': 'That list belongs to the next row.'},
        'hint': "The coefficients of (a+b)^n come from row n of Pascal's Triangle. Build row 5 "
                'from row 4 by adding adjacent entries and placing 1 at both ends.'},
 'q8': {'answer': 'C',
        'feedback': {'A': 'Check the factorial simplification carefully.',
                     'B': 'Remember to divide by both 3! and 4!.',
                     'D': 'The binomial coefficient is not simply n.'},
        'hint': 'Use n choose k = n!/[k!(n-k)!]. For 7 choose 3, simplify 7!/(3!4!).'},
 'q9': {'answer': 'A',
        'feedback': {'B': 'The middle terms do not disappear in a binomial expansion.',
                     'C': "Check the middle coefficient in row 4 of Pascal's Triangle.",
                     'D': 'The x³ and x terms are also part of the expansion.'},
        'hint': "Use row 4 of Pascal's Triangle: 1, 4, 6, 4, 1. Pair those coefficients with "
                'descending powers of x and ascending powers of 1.'},
 'q10': {'answer': 'D',
         'feedback': {'A': '6 is the binomial coefficient, but you must also include 3².',
                      'B': 'Check the power of 3 associated with the x² term.',
                      'C': 'Include the binomial coefficient C(4,2).'},
         'hint': 'The x² term corresponds to k=2 in (x+3)^4. Compute C(4,2)·x²·3² and identify the '
                 'numerical coefficient.'},
 'q11': {'answer': 'B',
         'feedback': {'A': 'This is the expansion of (x+1)^3; account for the negative term.',
                      'C': 'Because (-1)² is positive, the x term should be positive.',
                      'D': 'Check the signs of the x² and x terms.'},
         'hint': 'Write (x-1)^3 as (x+(-1))^3. Track the powers of -1: -1, +1, -1.'},
 'q12': {'answer': 'C',
         'feedback': {'A': 'You used the binomial coefficient but omitted the factor 3².',
                      'B': 'Check the power of 3 in the third term.',
                      'D': 'For the third term, the power of x should be 5-2=3.'},
         'hint': 'The 3rd term corresponds to k=2. Use C(5,2)x^(5-2)3².'},
 'q13': {'answer': 'A',
         'feedback': {'B': '36 is 6², but row sums follow powers of 2.',
                      'C': 'Use the row-sum identity 2^n.',
                      'D': 'Use the row-sum identity 2^n.'},
         'hint': "The sum of the entries in row n of Pascal's Triangle is 2^n. Here n=6."}}


def _is_nbgrader_execution() -> bool:
    return os.environ.get("NBGRADER_EXECUTION", "").lower() in {"autograde", "validate"}


def _box(message: str, kind: str = "info") -> None:
    styles = {
        "success": ("#e8f5e9", "#2e7d32"),
        "error": ("#ffebee", "#c62828"),
        "warning": ("#fff8e1", "#8d6e00"),
        "info": ("#e3f2fd", "#1565c0"),
    }
    bg, border = styles.get(kind, styles["info"])
    display(HTML(
        f'<div style="padding:10px 12px;margin:6px 0;border-left:4px solid {border};'
        f'background:{bg};border-radius:4px;">{message}</div>'
    ))


def check_answer(question_id: str, student_answer) -> None:
    """Formative multiple-choice feedback. nbgrader remains authoritative."""
    if _is_nbgrader_execution():
        return None

    if question_id not in QUESTION_FEEDBACK:
        _box(f"Unknown question ID: {escape(str(question_id))}", "warning")
        return None

    answer = "" if student_answer is None else str(student_answer).strip().upper()
    if not answer:
        _box("⚠️ Please enter an answer (A, B, C, or D) inside the quotation marks, then run the cell again.", "warning")
        return None

    if answer not in {"A", "B", "C", "D"}:
        _box("⚠️ Please enter only A, B, C, or D.", "warning")
        return None

    cfg = QUESTION_FEEDBACK[question_id]
    if answer == cfg["answer"]:
        _box("✅ <strong>Correct — good job!</strong>", "success")
        return None

    feedback = cfg["feedback"].get(answer, "Review the question and try again.")
    hint = cfg["hint"]
    _box(
        "❌ <strong>Not quite. Try again.</strong><br>"
        f"{escape(feedback)}<br><small><strong>Hint:</strong> {escape(hint)}</small>",
        "error",
    )
    return None


def check_code_answer(question_id: str, function) -> None:
    """Formative feedback for the RA6 Pascal's Triangle coding question."""
    if _is_nbgrader_execution():
        return None

    if question_id != "q14":
        _box(f"Unknown code question ID: {escape(str(question_id))}", "warning")
        return None

    if not callable(function):
        _box("⚠️ Keep the function named pascal_row(n), complete its body, and run the cell again.", "warning")
        return None

    test_rows = (0, 2, 4, 6)
    try:
        values = [function(n) for n in test_rows]
    except Exception as exc:
        _box(
            "❌ <strong>Not quite. Try again.</strong><br>"
            f"Your function produced an error: {escape(str(exc))}<br>"
            "<small><strong>Hint:</strong> Return a list of binomial coefficients for row n.</small>",
            "error",
        )
        return None

    if not all(isinstance(v, list) for v in values):
        _box(
            "❌ <strong>Not quite. Try again.</strong><br>"
            "Your function should return a list for each row.<br>"
            "<small><strong>Hint:</strong> Use a return statement inside pascal_row(n).</small>",
            "error",
        )
        return None

    expected = [[math.comb(n, k) for k in range(n + 1)] for n in test_rows]
    if all(got == want for got, want in zip(values, expected)):
        _box("✅ <strong>Correct — good job!</strong>", "success")
        return None

    _box(
        "❌ <strong>Not quite. Try again.</strong><br>"
        "Your function returns lists, but some Pascal's Triangle entries are incorrect.<br>"
        "<small><strong>Hint:</strong> Row n has n + 1 entries, with entry k equal to math.comb(n, k).</small>",
        "error",
    )
    return None
