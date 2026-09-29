from __future__ import annotations

import os
from html import escape
from IPython.display import display, HTML


QUESTION_FEEDBACK = {
    "q1": {
        "answer": "C",
        "feedback": {
            "A": "You differentiated r², but related rates also requires the Chain Rule factor dr/dt.",
            "B": "The derivative of r² is 2r, not r².",
            "D": "The factor r is missing after differentiating r².",
        },
        "hint": "Differentiate A = πr² with respect to time t. Since r depends on t, use the Chain Rule.",
    },
    "q2": {
        "answer": "B",
        "feedback": {
            "A": "This uses 2s but does not multiply by the given rate ds/dt = 2.",
            "C": "This is s², the area itself, rather than the rate dA/dt.",
            "D": "Use dA/dt = 2s(ds/dt), then substitute s = 5 and ds/dt = 2.",
        },
        "hint": "Differentiate A = s² first: dA/dt = 2s(ds/dt). Then substitute the given values.",
    },
    "q3": {
        "answer": "A",
        "feedback": {
            "B": "Differentiate r³ before substituting. The factor 3 cancels the 1/3 in the volume formula.",
            "C": "After differentiating, dV/dt = 4πr²(dr/dt). Remember to use r = 2.",
            "D": "Check r² when r = 2 and then multiply by 4π and dr/dt.",
        },
        "hint": "Differentiate V = (4/3)πr³ with respect to t to get dV/dt = 4πr²(dr/dt).",
    },
    "q4": {
        "answer": "D",
        "feedback": {
            "A": "The magnitude is right, but the sign should be negative because the top of the ladder is moving downward.",
            "B": "First use x² + y² = 169 with x = 5 to find y, then differentiate the equation.",
            "C": "dx/dt = 2 ft/s is the horizontal rate, not the vertical rate being requested.",
        },
        "hint": "When x = 5, y = 12. Differentiate x² + y² = 169: 2x(dx/dt) + 2y(dy/dt) = 0.",
    },
    "q5": {
        "answer": "A",
        "feedback": {
            "B": "The rates do not simply add. Differentiate x² + y² = z².",
            "C": "Use the current distances x = 4, y = 3, so z = 5, together with both velocity components.",
            "D": "This is too large; after differentiating, divide by z.",
        },
        "hint": "Differentiate x² + y² = z²: x(dx/dt) + y(dy/dt) = z(dz/dt). Here z = 5.",
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
    """Formative multiple-choice feedback. nbgrader remains authoritative."""
    if _is_nbgrader_execution():
        return None

    if question_id not in QUESTION_FEEDBACK:
        _box(f"Unknown question ID: {escape(str(question_id))}", "warning")
        return None

    if student_answer is None:
        answer = ""
    else:
        answer = str(student_answer).strip().upper()

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
    hint = cfg["hint"]
    _box(
        "❌ <strong>Not quite. Try again.</strong><br>"
        f"{escape(feedback)}<br><small><strong>Hint:</strong> {escape(hint)}</small>",
        "error",
    )
    return None


def check_code_answer(question_id: str, function) -> None:
    """Formative feedback for the RA6 coding question."""
    if _is_nbgrader_execution():
        return None

    if question_id != "q6":
        _box(f"Unknown code question ID: {escape(str(question_id))}", "warning")
        return None

    if not callable(function):
        _box("⚠️ Keep the function named dA_dt(r), complete its body, and run the cell again.", "warning")
        return None

    try:
        values = [function(r) for r in (1, 5, 10)]
    except Exception as exc:
        _box(
            "❌ <strong>Not quite. Try again.</strong><br>"
            f"Your function produced an error: {escape(str(exc))}<br>"
            "<small><strong>Hint:</strong> Differentiate A = πr² first, then substitute dr/dt = 3.</small>",
            "error",
        )
        return None

    if not all(isinstance(v, (int, float)) for v in values):
        _box(
            "❌ <strong>Not quite. Try again.</strong><br>"
            "Your function should return a number.<br>"
            "<small><strong>Hint:</strong> Use a return statement inside dA_dt(r).</small>",
            "error",
        )
        return None

    expected = [2 * 3.141592653589793 * r * 3 for r in (1, 5, 10)]
    if all(abs(v - e) < 1e-9 for v, e in zip(values, expected)):
        _box("✅ <strong>Correct — good job!</strong>", "success")
        return None

    _box(
        "❌ <strong>Not quite. Try again.</strong><br>"
        "Your function returns numbers, but the related-rates calculation is not correct yet.<br>"
        "<small><strong>Hint:</strong> dA/dt = 2πr(dr/dt), and dr/dt = 3 m/min.</small>",
        "error",
    )
    return None
