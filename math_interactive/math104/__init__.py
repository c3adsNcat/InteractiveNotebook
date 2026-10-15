from .ra6 import (
    check_answer as ra6_check_answer,
    check_code_answer as ra6_check_code_answer,
)

from .ra7 import (
    check_answer as ra7_check_answer,
    check_code_answer as ra7_check_code_answer,
)


def check_answer(question_id, student_answer):
    """Route multiple-choice feedback to the correct assignment."""
    if question_id in {"q7", "q8", "q9", "q10", "q11", "q12", "q13"}:
        return ra6_check_answer(question_id, student_answer)

    if question_id in {"q15", "q16", "q17", "q18", "q19"}:
        return ra7_check_answer(question_id, student_answer)

    raise ValueError(f"Unknown multiple-choice question ID: {question_id}")


def check_code_answer(question_id, function):
    """Route coding feedback to the correct assignment."""
    if question_id == "q14":
        return ra6_check_code_answer(question_id, function)

    if question_id == "q20":
        return ra7_check_code_answer(question_id, function)

    raise ValueError(f"Unknown coding question ID: {question_id}")


__all__ = [
    "check_answer",
    "check_code_answer",
]
