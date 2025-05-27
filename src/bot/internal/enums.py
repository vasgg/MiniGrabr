from enum import StrEnum, auto


class OrderStatus(StrEnum):
    DRAFT = auto()
    PUBLISHED = auto()
    WIP = auto()
    DELETED = auto()
    DONE = auto()


class UserType(StrEnum):
    CUSTOMER = auto()
    TRAVELER = auto()


class MenuButton(StrEnum):
    MAIN_MENU = auto()
    CLOSE = auto()
    BACK = auto()
    DELETE = auto()


class Crud(StrEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()


class OrderAction(StrEnum):
    TAKE = auto()
    SHOW_SENDER = auto()
