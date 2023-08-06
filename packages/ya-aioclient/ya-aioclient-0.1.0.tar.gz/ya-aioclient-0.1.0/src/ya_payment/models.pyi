from typing import Optional, List
from datetime import datetime
from typing_extensions import Literal

class InvoiceEvent(object):
    invoice_id: str  # readonly: False
    timestamp: datetime  # readonly: False
    details: dict  # readonly: False
    event_type: EventType  # readonly: False

    def __init__(self,
        invoice_id: str,
        timestamp: datetime,
        event_type: EventType,
        details: dict = None
    ) -> None: ...


class DebitNote(object):
    debit_note_id: str  # readonly: True
    issuer_id: str  # readonly: True
    recipient_id: str  # readonly: True
    payee_addr: Optional[str]  # readonly: True
    payer_addr: Optional[str]  # readonly: True
    previous_debit_note_id: Optional[str]  # readonly: True
    timestamp: datetime  # readonly: True
    agreement_id: str  # readonly: True
    activity_id: str  # readonly: False
    total_amount_due: str  # readonly: False
    usage_counter_vector: dict  # readonly: False
    payment_due_date: Optional[datetime]  # readonly: False
    status: InvoiceStatus  # readonly: False

    def __init__(self,
        activity_id: str,
        total_amount_due: str,
        status: InvoiceStatus,
        usage_counter_vector: dict = None,
        payment_due_date: Optional[datetime] = None
    ) -> None: ...


class Rejection(object):
    rejection_reason: RejectionReason  # readonly: False
    total_amount_accepted: str  # readonly: False
    message: Optional[str]  # readonly: False

    def __init__(self,
        rejection_reason: RejectionReason,
        total_amount_accepted: str,
        message: Optional[str] = None
    ) -> None: ...


class InvoiceStatus(object):

    def __init__(self) -> None: ...


class Payment(object):
    payment_id: str  # readonly: False
    payer_id: str  # readonly: False
    payee_id: str  # readonly: False
    payer_addr: Optional[str]  # readonly: False
    payee_addr: Optional[str]  # readonly: False
    amount: str  # readonly: False
    timestamp: datetime  # readonly: False
    allocation_id: Optional[str]  # readonly: False
    agreement_payments: array  # readonly: False
    activity_payments: array  # readonly: False
    details: str  # readonly: False

    def __init__(self,
        payment_id: str,
        payer_id: str,
        payee_id: str,
        amount: str,
        timestamp: datetime,
        agreement_payments: array,
        activity_payments: array,
        details: str,
        payer_addr: Optional[str] = None,
        payee_addr: Optional[str] = None,
        allocation_id: Optional[str] = None
    ) -> None: ...


class RejectionReason(object):

    def __init__(self) -> None: ...


class Allocation(object):
    allocation_id: str  # readonly: True
    total_amount: str  # readonly: False
    spent_amount: str  # readonly: True
    remaining_amount: str  # readonly: True
    timeout: Optional[datetime]  # readonly: False
    make_deposit: boolean  # readonly: False

    def __init__(self,
        total_amount: str,
        make_deposit: boolean,
        timeout: Optional[datetime] = None
    ) -> None: ...


class AgreementPayment(object):
    agreement_id: str  # readonly: False
    amount: str  # readonly: False

    def __init__(self,
        agreement_id: str,
        amount: str
    ) -> None: ...


class DebitNoteEvent(object):
    debit_note_id: str  # readonly: False
    timestamp: datetime  # readonly: False
    details: dict  # readonly: False
    event_type: EventType  # readonly: False

    def __init__(self,
        debit_note_id: str,
        timestamp: datetime,
        event_type: EventType,
        details: dict = None
    ) -> None: ...


class ErrorMessage(object):
    message: Optional[str]  # readonly: False

    def __init__(self,
        message: Optional[str] = None
    ) -> None: ...


class EventType(object):

    def __init__(self) -> None: ...


class ActivityPayment(object):
    activity_id: str  # readonly: False
    amount: str  # readonly: False

    def __init__(self,
        activity_id: str,
        amount: str
    ) -> None: ...


class Invoice(object):
    invoice_id: str  # readonly: True
    issuer_id: str  # readonly: True
    recipient_id: str  # readonly: True
    payee_addr: Optional[str]  # readonly: True
    payer_addr: Optional[str]  # readonly: True
    last_debit_note_id: Optional[str]  # readonly: True
    timestamp: datetime  # readonly: True
    agreement_id: str  # readonly: False
    activity_ids: array  # readonly: False
    amount: str  # readonly: False
    payment_due_date: datetime  # readonly: False
    status: InvoiceStatus  # readonly: False

    def __init__(self,
        agreement_id: str,
        amount: str,
        payment_due_date: datetime,
        status: InvoiceStatus,
        activity_ids: array = None
    ) -> None: ...


class Acceptance(object):
    total_amount_accepted: str  # readonly: False
    allocation_id: str  # readonly: False

    def __init__(self,
        total_amount_accepted: str,
        allocation_id: str
    ) -> None: ...


