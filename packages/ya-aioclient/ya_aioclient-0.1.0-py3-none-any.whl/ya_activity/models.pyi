from typing import Optional, List
from datetime import datetime
from typing_extensions import Literal

class ExeScriptCommandResult(object):
    index: integer  # readonly: False
    result: Literal["Ok","Error"]  # readonly: False
    message: Optional[str]  # readonly: False
    is_batch_finished: boolean  # readonly: False

    def __init__(self,
        index: integer,
        result: Literal["Ok","Error"],
        message: Optional[str] = None,
        is_batch_finished: boolean = None
    ) -> None: ...


class ActivityState(object):
    state: array  # readonly: False
    reason: Optional[str]  # readonly: False
    error_message: Optional[str]  # readonly: False

    def __init__(self,
        state: array,
        reason: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> None: ...


class ActivityUsage(object):
    current_usage: array  # readonly: False
    timestamp: integer  # readonly: False

    def __init__(self,
        current_usage: array = None,
        timestamp: integer = None
    ) -> None: ...


class ProviderEvent(object):
    event_type: str  # readonly: False
    activity_id: str  # readonly: False

    def __init__(self,
        event_type: str,
        activity_id: str
    ) -> None: ...


class ExeScriptRequest(object):
    text: str  # readonly: False

    def __init__(self,
        text: str
    ) -> None: ...


class ExeScriptCommandState(object):
    command: str  # readonly: False
    progress: Optional[str]  # readonly: False
    params: array  # readonly: False

    def __init__(self,
        command: str,
        progress: Optional[str] = None,
        params: array = None
    ) -> None: ...


class ErrorMessage(object):
    message: Optional[str]  # readonly: False

    def __init__(self,
        message: Optional[str] = None
    ) -> None: ...


class CreateActivityAllOf(ProviderEvent):
    agreement_id: Optional[str]  # readonly: False

    def __init__(self,
        event_type: str,
        activity_id: str,
        agreement_id: Optional[str] = None
    ) -> None: ...


class DestroyActivity(ProviderEvent):
    agreement_id: Optional[str]  # readonly: False

    def __init__(self,
        event_type: str,
        activity_id: str,
        agreement_id: Optional[str] = None
    ) -> None: ...


class CreateActivity(ProviderEvent):
    agreement_id: Optional[str]  # readonly: False

    def __init__(self,
        event_type: str,
        activity_id: str,
        agreement_id: Optional[str] = None
    ) -> None: ...


