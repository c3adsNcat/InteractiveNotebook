from __future__ import annotations

import os
from html import escape

import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import clear_output, display, HTML


QUESTION_FEEDBACK = {
    "q1": {
        "answer": "A",
        "feedback": {
            "B": "You applied f first. For f∘g, apply g first.",
            "C": "Check the substitution carefully: f(u) = u + 4.",
            "D": "Composition means substitution, not multiplication.",
        },
        "hint": "Composition means f(g(x)). Start with g(x) = x², then substitute it into f.",
    },
    "q2": {
        "answer": "C",
        "feedback": {
            "A": "The square-root input cannot be negative.",
            "B": "Check the direction of the inequality x - 5 ≥ 0.",
            "D": "Remember that √0 is defined, so the endpoint is included.",
        },
        "hint": "A square root requires its input to be at least 0. Solve x - 5 ≥ 0.",
    },
    "q3": {
        "answer": "C",
        "feedback": {
            "A": "x² fails the horizontal line test.",
            "B": "|x| gives the same output for x and -x.",
            "D": "x² - 4 still has the symmetry of a parabola.",
        },
        "hint": "Use the horizontal line test. A non-horizontal linear function is one-to-one.",
    },
    "q4": {
        "answer": "C",
        "feedback": {
            "A": "A shift does not interchange x- and y-coordinates.",
            "B": "Reflection across the x-axis changes y to -y.",
            "D": "Reflection across the y-axis changes x to -x.",
        },
        "hint": "An inverse swaps the x- and y-coordinates of each point.",
    },
    "exp1": {
        "answer": "C",
        "feedback": {
            "A": "Check the value of 2³.",
            "B": "Remember that 2³ = 8.",
            "D": "Compute 6 × 8 carefully.",
        },
        "hint": "Substitute x = 3 into f(x) = 6·2ˣ. Compute 2³ first, then multiply by 6.",
    },
    "exp2": {
        "answer": "C",
        "feedback": {
            "A": "A base greater than 1 gives exponential growth.",
            "B": "1.5 is greater than 1, so this is growth.",
            "D": "This is a quadratic function, not an exponential function.",
        },
        "hint": "For exponential decay, the exponential base must be between 0 and 1.",
    },
}


def _is_nbgrader_execution():
    """True when nbgrader is executing the notebook non-interactively."""
    return os.environ.get("NBGRADER_EXECUTION", "").lower() in {"autograde", "validate"}


def check_answer(question_id, student_answer):
    """
    Give immediate formative feedback for a multiple-choice response.

    The student's *_final variable is the single source of truth:
        q2_final = "C"
        check_answer("q2", q2_final)

    During nbgrader autograde/validate, formative feedback is suppressed.
    Official grading should be performed by nbgrader tests against the
    same *_final variable.
    """
    if _is_nbgrader_execution():
        return None

    if question_id not in QUESTION_FEEDBACK:
        raise KeyError(f"Unknown question ID: {question_id}")

    cfg = QUESTION_FEEDBACK[question_id]
    answer = "" if student_answer is None else str(student_answer).strip().upper()

    if answer == "":
        display(HTML(
            '<div style="padding:10px;border-left:4px solid #d9a400;margin-top:6px;">'
            '⚠️ <b>Please enter an answer.</b><br>'
            'Enter A, B, C, or D, then run this cell again.'
            '</div>'
        ))
        return None

    if answer not in {"A", "B", "C", "D"}:
        display(HTML(
            '<div style="padding:10px;border-left:4px solid #d9a400;margin-top:6px;">'
            '⚠️ <b>Please enter only A, B, C, or D.</b>'
            '</div>'
        ))
        return None

    if answer == cfg["answer"]:
        display(HTML(
            '<div style="padding:10px;border-left:4px solid #2e8b57;margin-top:6px;">'
            '✅ <b>Correct — good job!</b>'
            '</div>'
        ))
        return None

    specific = cfg.get("feedback", {}).get(answer, "Review your work and try again.")
    hint = cfg.get("hint", "Review the question and try again.")

    display(HTML(
        '<div style="padding:10px;border-left:4px solid #c94c4c;margin-top:6px;">'
        '❌ <b>Not quite. Try again.</b><br><br>'
        f'{escape(specific)}<br><br>'
        f'💡 <b>Hint:</b> {escape(hint)}'
        '</div>'
    ))
    return None


def inverse_explorer():
    if _is_nbgrader_execution():
        return None

    slope = widgets.FloatSlider(
        value=2.0, min=0.5, max=3.0, step=0.5,
        description="slope", continuous_update=False
    )
    intercept = widgets.IntSlider(
        value=1, min=-5, max=5, step=1,
        description="intercept", continuous_update=False
    )
    output = widgets.Output()

    def redraw(_change=None):
        with output:
            clear_output(wait=True)
            x = np.linspace(-10, 10, 400)
            a, b = slope.value, intercept.value
            y = a*x + b
            y_inv = (x-b)/a

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(x, y, label=r"$f(x)$", linewidth=2)
            ax.plot(x, y_inv, "--", label=r"$f^{-1}(x)$", linewidth=2)
            ax.plot(x, x, ":", label=r"$y=x$")
            ax.axhline(0, linewidth=0.8)
            ax.axvline(0, linewidth=0.8)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title("A Function and Its Inverse")
            ax.grid(True)
            ax.legend()
            display(fig)
            plt.close(fig)

    slope.observe(redraw, names="value")
    intercept.observe(redraw, names="value")
    redraw()

    return widgets.VBox([
        widgets.HTML("<b>Explore:</b> Move the sliders and compare the function with its inverse."),
        widgets.HBox([slope, intercept]),
        output,
    ])
