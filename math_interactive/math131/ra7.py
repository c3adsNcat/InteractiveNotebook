from __future__ import annotations

import os
from html import escape
from IPython.display import display, HTML

QUESTION_FEEDBACK = {
    "q7": {
        "answer": 'B',
        "feedback": {
            'A': 'At x = 0, the second derivative is not zero.',
            'C': "x = 4 does not solve f''(x)=0.",
            'D': 'Recheck the derivative of the -6x² term.',
        },
        "hint": "Compute f''(x) and find where its sign changes.",
    },
    "q8": {
        "answer": 'A',
        "feedback": {
            'B': 'This is the concave-down interval, not concave-up.',
            'C': 'The second derivative changes sign within this interval.',
            'D': "Recalculate f''(x) = -6x + 6.",
        },
        "hint": "Compute f''(x); concave up means f''(x) > 0.",
    },
    "q9": {
        "answer": 'D',
        "feedback": {
            'A': 'A positive second derivative means a minimum, not a maximum.',
            'B': 'The test at x = 2 gives a positive second derivative.',
            'C': 'The second derivative test is conclusive here.',
        },
        "hint": "Evaluate f''(2). A positive second derivative at a critical point indicates a local minimum.",
    },
    "q10": {
        "answer": 'C',
        "feedback": {
            'A': "Use the sign changes of both f' and f''.",
            'B': "Check the change in f' at x = -1 and x = 3.",
            'D': 'Check the concavity switch at x = 1.',
        },
        "hint": "Match the sign changes of f' with extrema and the sign changes of f'' with concavity.",
    },
    "q11": {
        "answer": 'B',
        "feedback": {
            'A': "At x = 0, f' does not switch from negative to positive.",
            'C': "A local minimum occurs where f' changes from negative to positive.",
            'D': "Inspect the sign of f' around x = 3.",
        },
        "hint": "Use the sign of f' on either side of each critical number.",
    },
}

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
    """Formative multiple-choice feedback; nbgrader remains authoritative."""
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
    feedback = cfg["feedback"].get(answer, "Review the setup and try the calculation again.")
    _box(
        "❌ <strong>Not quite. Try again.</strong><br>"
        f"{escape(feedback)}<br><small><strong>Hint:</strong> {escape(cfg['hint'])}</small>",
        "error",
    )
    return None

def check_code_answer(question_id: str, functions) -> None:
    """Formative feedback for RA7 coding question q12: two derivatives."""
    if _is_nbgrader_execution():
        return None
    if question_id != "q12":
        _box(f"Unknown code question ID: {escape(str(question_id))}", "warning")
        return None
    if not isinstance(functions, (tuple, list)) or len(functions) != 2 or not all(callable(f) for f in functions):
        _box("⚠️ Define both f_prime(x) and f_double_prime(x), then run this cell again.", "warning")
        return None
    first, second = functions
    try:
        xs = (0, 1, 2, 1.5, -1)
        actual_first = [first(x) for x in xs]
        actual_second = [second(x) for x in xs]
    except Exception as exc:
        _box("❌ <strong>Not quite. Try again.</strong><br>" + escape(str(exc)), "error")
        return None
    import numbers
    if not all(isinstance(v, numbers.Real) and not isinstance(v, bool) for v in actual_first + actual_second):
        _box("❌ Both functions should return numeric values. Use return statements.", "error")
        return None
    expected_first = [6*x**2 - 18*x + 12 for x in xs]
    expected_second = [12*x - 18 for x in xs]
    if all(abs(a-b) < 1e-8 for a,b in zip(actual_first, expected_first)) and all(abs(a-b) < 1e-8 for a,b in zip(actual_second, expected_second)):
        _box("✅ <strong>Correct — good job!</strong>", "success")
    else:
        _box("❌ <strong>Not quite. Try again.</strong><br>Check the power rule for each term, then differentiate again to obtain f''(x).", "error")
    return None
