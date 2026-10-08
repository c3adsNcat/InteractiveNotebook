
# Interactive feedback helpers for MATH 131

from . import ra6, ra7


def check_answer(question_id, student_answer):
    """Route multiple-choice feedback to the correct assignment."""

    if question_id in ra6.QUESTION_FEEDBACK:
        return ra6.check_answer(question_id, student_answer)

    if question_id in ra7.QUESTION_FEEDBACK:
        return ra7.check_answer(question_id, student_answer)

    raise ValueError(f"Unknown question ID: {question_id}")


def check_code_answer(question_id, function):
    """Route coding feedback to the correct assignment."""

    if question_id == "q6":
        return ra6.check_code_answer(question_id, function)

    if question_id == "q14":
        return ra7.check_code_answer(question_id, function)

    raise ValueError(f"Unknown coding question ID: {question_id}")


__all__ = [
    "check_answer",
    "check_code_answer",
]
