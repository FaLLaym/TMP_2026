from abc import ABC, abstractmethod
from datetime import datetime


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, base_price: float) -> float:
        pass


class RegularPricing(PricingStrategy):
    """Обычная цена без изменений"""
    def calculate_price(self, base_price: float) -> float:
        return base_price


class DiscountPricing(PricingStrategy):
    """Скидка в процентах"""
    def __init__(self, discount_percent: float):
        self.discount_percent = discount_percent

    def calculate_price(self, base_price: float) -> float:
        return base_price * (1 - self.discount_percent / 100)


class VipPricing(PricingStrategy):
    """VIP наценка"""
    def __init__(self, multiplier: float = 2.0):
        self.multiplier = multiplier

    def calculate_price(self, base_price: float) -> float:
        return base_price * self.multiplier


class EarlyBirdPricing(PricingStrategy):
    """Раннее бронирование: фиксированная скидка"""
    def __init__(self, discount_amount: float):
        self.discount_amount = discount_amount

    def calculate_price(self, base_price: float) -> float:
        return max(base_price - self.discount_amount, 0)


class DynamicPricing(PricingStrategy):
    """Динамическое ценообразование в зависимости от заполненности стадиона"""
    def __init__(self, sold_percentage: float):
        self.sold_percentage = sold_percentage

    def calculate_price(self, base_price: float) -> float:
        if self.sold_percentage > 80:
            return base_price * 1.5  # дефицит мест
        elif self.sold_percentage < 30:
            return base_price * 0.8  # стимулирование продаж
        return base_price


class Ticket:
    def __init__(self, match_name: str, seat: str, base_price: float, strategy: PricingStrategy):
        self.match_name = match_name
        self.seat = seat
        self.base_price = base_price
        self._strategy = strategy
        self._sold = False

    def set_pricing_strategy(self, strategy: PricingStrategy):
        """Динамическая смена стратегии"""
        self._strategy = strategy

    def get_final_price(self) -> float:
        return self._strategy.calculate_price(self.base_price)

    def sell(self):
        self._sold = True

    def __str__(self):
        status = "ПРОДАН" if self._sold else "ДОСТУПЕН"
        return (f"Билет: {self.match_name} | Место: {self.seat} | "
                f"Базовая цена: {self.base_price} руб. | "
                f"Итоговая: {self.get_final_price()} руб. | "
                f"Статус: {status}")


def demonstrate_strategy():
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНА «СТРАТЕГИЯ»")
    print("=" * 60)

    tickets = [
        Ticket("ЦСКА - Спартак", "Сектор A, ряд 5, место 12", 1500, RegularPricing()),
        Ticket("ЦСКА - Спартак", "Сектор A, ряд 5, место 13", 1500, DiscountPricing(25)),
        Ticket("ЦСКА - Спартак", "VIP Ложа, место 3", 1500, VipPricing(3.0)),
        Ticket("ЦСКА - Спартак", "Сектор B, ряд 2, место 8", 1500, EarlyBirdPricing(300)),
        Ticket("ЦСКА - Спартак", "Сектор C, ряд 10, место 5", 1500, DynamicPricing(85)),
    ]

    for ticket in tickets:
        print(ticket)

    print("\n--- ДИНАМИЧЕСКАЯ СМЕНА СТРАТЕГИИ ---")
    ticket = Ticket("Зенит - Локомотив", "Сектор D, место 1", 2000, RegularPricing())
    print(f"До смены: {ticket}")

    ticket.set_pricing_strategy(DiscountPricing(15))
    print(f"После смены (скидка 15%): {ticket}")

    ticket.set_pricing_strategy(VipPricing(2.5))
    print(f"После смены (VIP наценка 2.5x): {ticket}")


if __name__ == "__main__":
    demonstrate_strategy()