
from domain.ledger.category.category.entity import Category
from domain.ledger.category.item.entity import Item

class SummaryData:
    category: Category
    item:Item
    total_amount: int

    def __init__(self, category: Category, item: Item, total_amount: int) -> None:
        self.category = category
        self.item = item
        self.total_amount = total_amount