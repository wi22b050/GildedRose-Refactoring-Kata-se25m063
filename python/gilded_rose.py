from abc import ABC, abstractmethod
from typing import List

# SRP: Single Responsibility Principle

class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return f"{self.name}, {self.sell_in}, {self.quality}"


class ItemQualityUpdater(ABC):
    """OCP: Open for extension, closed for modification"""
    
    @abstractmethod
    def update_quality(self, item: Item):
        pass
    
    def _clamp_quality(self, item: Item):
        item.quality = max(0, min(50, item.quality))


class NormalItemUpdater(ItemQualityUpdater):
    def update_quality(self, item: Item):
        item.sell_in -= 1
        
        degrade_amount = 2 if item.sell_in < 0 else 1
        item.quality -= degrade_amount
        
        self._clamp_quality(item)


class AgedBrieUpdater(ItemQualityUpdater):
    def update_quality(self, item: Item):
        item.sell_in -= 1
        
        increase_amount = 2 if item.sell_in < 0 else 1
        item.quality += increase_amount
        
        self._clamp_quality(item)


class BackstagePassUpdater(ItemQualityUpdater):
    def update_quality(self, item: Item):
        item.sell_in -= 1
        
        if item.sell_in < 0:
            item.quality = 0
        elif item.sell_in < 5:
            item.quality += 3
        elif item.sell_in < 10:
            item.quality += 2
        else:
            item.quality += 1
            
        self._clamp_quality(item)


class SulfurasUpdater(ItemQualityUpdater):
    def update_quality(self, item: Item):
        pass


class ItemUpdater(ItemQualityUpdater):
    def update_quality(self, item: Item):
        item.sell_in -= 1
        
        degrade_amount = 2 if item.sell_in >= 0 else 4
        item.quality -= degrade_amount
        
        self._clamp_quality(item)


# DIP: Dependency Inversion Principle

class ItemUpdaterFactory:
    """Factory to create appropriate updaters - follows DIP"""
    
    _updaters = {
        "Aged Brie": AgedBrieUpdater,
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdater,
        "Sulfuras, Hand of Ragnaros": SulfurasUpdater,
        "Conjured Mana Cake": ItemUpdater
    }
    
    @classmethod
    def get_updater(cls, item_name: str) -> ItemQualityUpdater:
        updater_class = cls._updaters.get(item_name, NormalItemUpdater)
        return updater_class()


# KISS: Keep It Simple, Stupid

class GildedRose:
    def __init__(self, items: List[Item]):
        self.items = items
        self._factory = ItemUpdaterFactory()

    def update_quality(self):
        """DRY: No repeated code, each updater handles its own logic"""
        for item in self.items:
            updater = self._factory.get_updater(item.name)
            updater.update_quality(item)


if __name__ == "__main__":
    items = [
        Item("Aged Brie", 2, 0),
        Item("Backstage passes to a TAFKAL80ETC concert", 15, 20),
        Item("Sulfuras, Hand of Ragnaros", 0, 80),
        Item("Normal Item", 10, 20),
        Item("Conjured Mana Cake", 3, 6),
    ]
    
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    for item in items:
        print(item)