__all__ = (
    "BridgingDifferentTypesException",
    "DomainException",
    "InvalidVacationException",
    "NoWorkDaysException",
    "VacationAlreadyExistsException",
)


class DomainException(Exception):
    """
    Base exception for all domain errors
    """


class InvalidVacationException(DomainException):
    """
    Base exception for all invalid vacations
    """


class NoWorkDaysException(InvalidVacationException):
    """
    Raised when no work days present in vacation
    """


class VacationAlreadyExistsException(InvalidVacationException):
    """
    Raised when vacation already exists
    """


class BridgingDifferentTypesException(InvalidVacationException):
    """
    Raised when new vacation would bridge two existing vacations with different types
    """
