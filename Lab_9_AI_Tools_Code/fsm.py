from enum import Enum
from typing import Set, Dict


class ApplicationStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    IN_REVIEW = "IN_REVIEW"
    NEEDS_INFO = "NEEDS_INFO"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class InvalidStateTransitionError(Exception):
    """Исключение при попытке выполнить недопустимый переход в конечном автомате."""
    pass


class ScholarshipApplicationFSM:
    """
    Конечный автомат (FSM) управления жизненным циклом стипендиальной заявки.
    """

    ALLOWED_TRANSITIONS: Dict[ApplicationStatus, Set[ApplicationStatus]] = {
        ApplicationStatus.DRAFT: {
            ApplicationStatus.SUBMITTED
        },
        ApplicationStatus.SUBMITTED: {
            ApplicationStatus.IN_REVIEW,
            ApplicationStatus.DRAFT  # Студент может отозвать на редактирование
        },
        ApplicationStatus.IN_REVIEW: {
            ApplicationStatus.APPROVED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.NEEDS_INFO
        },
        ApplicationStatus.NEEDS_INFO: {
            ApplicationStatus.IN_REVIEW,  # Студент прикрепил недостающие справки
            ApplicationStatus.REJECTED    # Истёк срок досылки документов
        },
        ApplicationStatus.APPROVED: set(),  # Терминальное состояние
        ApplicationStatus.REJECTED: set(),  # Терминальное состояние
    }

    def __init__(self, application_id: int, initial_status: ApplicationStatus = ApplicationStatus.DRAFT):
        self.application_id = application_id
        self.status = initial_status

    def can_transit_to(self, target_status: ApplicationStatus) -> bool:
        return target_status in self.ALLOWED_TRANSITIONS.get(self.status, set())

    def transit_to(self, target_status: ApplicationStatus) -> None:
        if not self.can_transit_to(target_status):
            raise InvalidStateTransitionError(
                f"Недопустимый переход заявки #{self.application_id} из статуса '{self.status.value}' в '{target_status.value}'."
            )
        self.status = target_status
