"""MATH 104 RA7: Angles, Radians, and Right Triangle Trigonometry.

Formative feedback only; nbgrader hidden tests remain authoritative.
RA7 uses q15–q20; RA6 ends at q14.
"""
from __future__ import annotations

import os
import math
from html import escape
from IPython.display import display, HTML

QUESTION_FEEDBACK = {'q15': {'answer': 'C', 'feedback': {'A': '3π/4 radians corresponds to 135°, not 150°.', 'B': '2π/3 radians corresponds to 120°.', 'D': '5π/3 radians corresponds to 300°.'}, 'hint': 'Multiply degrees by π/180 and simplify 150π/180.'}, 'q16': {'answer': 'B', 'feedback': {'A': '18π is much larger than the arc of a circle with radius 6 and angle π/3.', 'C': 'The formula multiplies the radius and angle rather than dividing.', 'D': '6π would use an angle of π, not π/3.'}, 'hint': 'Use s = rθ with θ in radians: 6 × π/3.'}, 'q17': {'answer': 'D', 'feedback': {'A': 'Dividing radius by angular speed does not give linear speed.', 'B': 'Linear speed is radius multiplied by angular speed, not added.', 'C': 'This is the radius, not the speed.'}, 'hint': 'Use v = rω with r = 13 inches and ω = 4 radians/second.'}, 'q18': {'answer': 'A', 'feedback': {'B': '4/5 is cosine, adjacent divided by hypotenuse.', 'C': '3/4 is tangent, opposite divided by adjacent.', 'D': '5/3 is the reciprocal of sine.'}, 'hint': 'SOH: sin θ = opposite/hypotenuse. Here opposite = 3, hypotenuse = 5.'}, 'q19': {'answer': 'C', 'feedback': {'A': '12/13 is cosine, not tangent.', 'B': '13/12 is secant, not tangent.', 'D': '13/5 is cosecant, not tangent.'}, 'hint': 'With sin θ = 5/13, the adjacent side is sqrt(13²−5²) = 12. Then tan θ = opposite/adjacent.'}}


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
    """Formative feedback for RA7's find_height coding question."""
    if _is_nbgrader_execution():
        return None
    if question_id != "q20":
        _box(f"Unknown code question ID: {escape(str(question_id))}", "warning")
        return None
    if not callable(function):
        _box("⚠️ Keep the function named find_height(distance, angle_deg), complete its body, and run the cell again.", "warning")
        return None
    try:
        cases = [(100, 45), (50, 30), (80, 60)]
        values = [function(distance, angle) for distance, angle in cases]
    except Exception as exc:
        _box(
            "❌ <strong>Not quite. Try again.</strong><br>"
            f"Your function produced an error: {escape(str(exc))}<br>"
            "<small><strong>Hint:</strong> Convert degrees to radians before using math.tan.</small>",
            "error",
        )
        return None
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in values):
        _box("❌ <strong>Not quite.</strong> Return a finite number for each input.", "error")
        return None
    expected = [distance * math.tan(math.radians(angle)) for distance, angle in cases]
    if all(math.isclose(v, e, rel_tol=1e-9, abs_tol=1e-9) for v, e in zip(values, expected)):
        _box("✅ <strong>Correct — good job!</strong>", "success")
        return None
    _box(
        "❌ <strong>Not quite. Try again.</strong><br>"
        "Your function returns numbers, but the height calculation is not correct yet.<br>"
        "<small><strong>Hint:</strong> height = distance * math.tan(math.radians(angle_deg)).</small>",
        "error",
    )
    return None
