from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.organization.organization.entity import Organization

class LedgerOrganization(Organization):

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="ledger_organization"
    )
    items: Mapped[list["Item"]] = relationship(
        "Item",
        back_populates="ledger_organization"
    )
    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="ledger_organization"
    )
    receipts: Mapped[list["Receipt"]] = relationship(
        "Receipt",
        back_populates="ledger_organization"
    )

    __mapper_args__ = {
        "polymorphic_identity": "ledger_organization"
    }