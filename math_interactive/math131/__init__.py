
from .ra6 import (
    check_answer as ra6_check_answer,
    check_code_answer as ra6_check_code_answer,
)

from .ra7 import (
    check_answer as ra7_check_answer,
    check_code_answer as ra7_check_code_answer,
)

from .ra8 import (
    check_answer as ra8_check_answer,
)


def check_answer(question_id, student_answer, assignment=None):
    """
    Route interactive feedback to the correct assignment.

    RA6: q1-q5
    RA7: q7-q11
    RA8: q1-q5 (requires assignment="RA8")

    Existing RA6 and RA7 calls remain compatible.
    """

    question_id = str(question_id).lower()

    if assignment is not None:
        assignment = str(assignment).upper()

        if assignment == "RA6":
            return ra6_check_answer(question_id, student_answer)

        if assignment == "RA7":
            return ra7_check_answer(question_id, student_answer)

        if assignment == "RA8":
            return ra8_check_answer(question_id, student_answer)

        raise ValueError(
            f"Unknown assignment: {assignment}"
        )

    # Preserve existing behavior for RA6
    if question_id in {"q1", "q2", "q3", "q4", "q5"}:
        return ra6_check_answer(question_id, student_answer)

    # Preserve existing behavior for RA7
    if question_id in {"q7", "q8", "q9", "q10", "q11"}:
        return ra7_check_answer(question_id, student_answer)

    raise ValueError(
        f"Unknown question ID: {question_id}. "
        "For RA8, specify assignment='RA8'."
    )


def check_code_answer(question_id, function, assignment=None):
    """
    Route coding feedback to the correct assignment.
    """

    question_id = str(question_id).lower()

    if assignment is not None:
        assignment = str(assignment).upper()

        if assignment == "RA6":
            return ra6_check_code_answer(question_id, function)

        if assignment == "RA7":
            return ra7_check_code_answer(question_id, function)

        raise ValueError(
            f"No coding feedback configured for {assignment}"
        )

    if question_id == "q6":
        return ra6_check_code_answer(question_id, function)

    if question_id == "q12":
        return ra7_check_code_answer(question_id, function)

    raise ValueError(
        f"Unknown coding question ID: {question_id}"
    )


__all__ = [
    "check_answer",
    "check_code_answer",
]
