from catanatron.models.enums import Resource


class Deck:
    def __init__(self, card_types):
        """Provides functionality to manage a pack of cards.

        Args:
            card_types (Enum): Describes cards to use
        """
        self.card_types = card_types
        self.cards = {card: 0 for card in self.card_types}

    def includes(self, other):
        for card_type in self.card_types:
            if self.count(card_type) < other.count(card_type):
                return False
        return True

    def count(self, card_type):
        return self.cards[card_type]

    def num_cards(self):
        total = 0
        for card_type in self.card_types:
            total += self.count(card_type)
        return total

    def can_draw(self, count: int, card_type):
        return self.count(card_type) >= count

    def draw(self, count: int, card_type):
        if not self.can_draw(count, card_type):
            raise ValueError(f"Cant draw {count} {card_type}. Not enough cards.")

        self.cards[card_type] -= count

    def replenish(self, count: int, card_type):
        self.cards[card_type] += count

    def to_array(self):
        """Make it look like a deck of cards"""
        array = []
        for card_type in self.card_types:
            array.extend([card_type] * self.count(card_type))
        return array

    def __add__(self, other):
        for card_type in self.card_types:
            self.replenish(other.count(card_type), card_type)
        return self

    def __sub__(self, other):
        for card_type in self.card_types:
            self.draw(other.count(card_type), card_type)
        return self


class ResourceDeck(Deck):
    @staticmethod
    def starting_bank():
        deck = ResourceDeck()
        deck.replenish(19, Resource.WOOD)
        deck.replenish(19, Resource.BRICK)
        deck.replenish(19, Resource.SHEEP)
        deck.replenish(19, Resource.WHEAT)
        deck.replenish(19, Resource.ORE)
        return deck

    @staticmethod
    def road_cost():
        deck = ResourceDeck()
        deck.replenish(1, Resource.WOOD)
        deck.replenish(1, Resource.BRICK)
        return deck

    @staticmethod
    def settlement_cost():
        deck = ResourceDeck()
        deck.replenish(1, Resource.WOOD)
        deck.replenish(1, Resource.BRICK)
        deck.replenish(1, Resource.SHEEP)
        deck.replenish(1, Resource.WHEAT)
        return deck

    @staticmethod
    def city_cost():
        deck = ResourceDeck()
        deck.replenish(2, Resource.WHEAT)
        deck.replenish(3, Resource.ORE)
        return deck

    def __init__(self):
        Deck.__init__(self, Resource)
