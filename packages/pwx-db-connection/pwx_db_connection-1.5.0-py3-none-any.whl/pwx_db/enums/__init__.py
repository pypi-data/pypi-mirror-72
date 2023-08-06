from enum import Enum, unique


@unique
class InstanceStatusIntEnum(Enum):
    SUCCESS = 5
    NODATA = 1
    WARNING = 4
    TIMEOUT = 3
    FAIL = 2


@unique
class InstanceStateIntEnum(Enum):
    NORMAL = 1
    MAINTENANCE_NO_DATA_COLLECTION = 2
    MAINTENANCE_WITH_DATA_COLLECTION = 3
    STRESS = 4


@unique
class StepTypeEnum(Enum):
    USER = 1
    SYSTEM = 2
    SETUP = 3
    TEARDOWN = 4


@unique
class TimeoutMessagesEnum(Enum):
    NOT_VISIBLE_AFTER = 'not visible after'
    TIMEOUT_LOADING_PAGE_AFTER = 'Timeout loading pager after'
    KEYWORD_TIMEOUT = 'Keyword timeout'
    TIMEOUT_EXCEPTION = 'TimeoutException'


__all__ = ['InstanceStateIntEnum', 'StepTypeEnum', 'TimeoutMessagesEnum', 'InstanceStatusIntEnum']
