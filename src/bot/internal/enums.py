from enum import StrEnum, auto


class MenuButtons(StrEnum):
    BACK = auto()


class OrderStatus(StrEnum):
    DRAFT = auto()
    PUBLISHED = auto()
    WIP = auto()
    DELETED = auto()
    DONE = auto()


class UserType(StrEnum):
    CUSTOMER = auto()
    TRAVELER = auto()


class CustomerAction(StrEnum):
    CREATE_ORDER = auto()
    MY_ORDERS = auto()
    FIND_TRAVELER = auto()


class TravelerAction(StrEnum):
    CREATE_TRIP = auto()
    FIND_ORDERS = auto()
    MY_RESPONSES = auto()
