import pytest
from fsm import ScholarshipApplicationFSM, ApplicationStatus, InvalidStateTransitionError


def test_happy_path_lifecycle():
    fsm = ScholarshipApplicationFSM(application_id=101)
    assert fsm.status == ApplicationStatus.DRAFT

    fsm.transit_to(ApplicationStatus.SUBMITTED)
    assert fsm.status == ApplicationStatus.SUBMITTED

    fsm.transit_to(ApplicationStatus.IN_REVIEW)
    assert fsm.status == ApplicationStatus.IN_REVIEW

    fsm.transit_to(ApplicationStatus.APPROVED)
    assert fsm.status == ApplicationStatus.APPROVED


def test_cycle_with_needs_info():
    fsm = ScholarshipApplicationFSM(application_id=102, initial_status=ApplicationStatus.IN_REVIEW)

    # Деканат запрашивает уточнения
    fsm.transit_to(ApplicationStatus.NEEDS_INFO)
    assert fsm.status == ApplicationStatus.NEEDS_INFO

    # Студент предоставил документы -> возврат на проверку
    fsm.transit_to(ApplicationStatus.IN_REVIEW)
    assert fsm.status == ApplicationStatus.IN_REVIEW

    # Отклонение заявки
    fsm.transit_to(ApplicationStatus.REJECTED)
    assert fsm.status == ApplicationStatus.REJECTED


def test_invalid_transitions_raise_error():
    fsm = ScholarshipApplicationFSM(application_id=103, initial_status=ApplicationStatus.DRAFT)

    # Нельзя перепрыгнуть из DRAFT сразу в APPROVED
    with pytest.raises(InvalidStateTransitionError, match="Недопустимый переход"):
        fsm.transit_to(ApplicationStatus.APPROVED)

    # Нельзя перейти из DRAFT сразу в IN_REVIEW
    with pytest.raises(InvalidStateTransitionError):
        fsm.transit_to(ApplicationStatus.IN_REVIEW)


def test_terminal_state_immutable():
    fsm = ScholarshipApplicationFSM(application_id=104, initial_status=ApplicationStatus.APPROVED)

    # Из APPROVED нельзя никуда перейти
    with pytest.raises(InvalidStateTransitionError):
        fsm.transit_to(ApplicationStatus.IN_REVIEW)
    with pytest.raises(InvalidStateTransitionError):
        fsm.transit_to(ApplicationStatus.DRAFT)
