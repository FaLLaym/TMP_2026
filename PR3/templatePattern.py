from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
from datetime import datetime


class ReportGenerator(ABC):
    """
    Абстрактный класс, определяющий скелет алгоритма генерации отчета.
    Шаблонный метод generate() вызывает последовательность шагов.
    """

    def generate(self, data: List[Dict[str, Any]]) -> str:
        """
        Шаблонный метод (Template Method).
        Определяет структуру алгоритма, не изменяемую для всех подклассов.
        """
        # Шаг 1: Подготовка данных (может быть переопределен)
        prepared_data = self._prepare_data(data)

        # Шаг 2: Форматирование данных (обязателен для реализации)
        formatted_content = self._format_data(prepared_data)

        # Шаг 3: Добавление заголовка (hook - может быть переопределен)
        header = self._add_header()

        # Шаг 4: Добавление подвала (hook - может быть переопределен)
        footer = self._add_footer()

        # Сборка финального отчета
        return self._assemble_report(header, formatted_content, footer)

    def _prepare_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Общий шаг: подготовка данных.
        Может быть переопределен в подклассах, если нужна особая подготовка.
        """
        # Базовый шаг: сортировка по дате продажи
        return sorted(data, key=lambda x: x.get('sale_date', ''), reverse=True)

    @abstractmethod
    def _format_data(self, data: List[Dict[str, Any]]) -> str:
        """
        Абстрактный метод: форматирование данных.
        Каждый подкласс реализует свой формат.
        """
        pass

    def _add_header(self) -> str:
        """
        Hook метод: добавление заголовка.
        По умолчанию возвращает пустую строку, может быть переопределен.
        """
        return ""

    def _add_footer(self) -> str:
        """
        Hook метод: добавление подвала.
        По умолчанию возвращает дату генерации отчета.
        """
        return f"\nОтчет сгенерирован: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def _assemble_report(self, header: str, content: str, footer: str) -> str:
        """
        Сборка финального отчета.
        Может быть переопределен для изменения структуры.
        """
        parts = []
        if header:
            parts.append(header)
        parts.append(content)
        if footer:
            parts.append(footer)
        return "\n".join(parts)


class HTMLReportGenerator(ReportGenerator):
    """Генератор отчета в формате HTML"""

    def _add_header(self) -> str:
        return """<!DOCTYPE html>
<html>
<head><title>Отчет о продажах билетов</title></head>
<body>
<h1>Отчет о продажах билетов на футбол</h1>
<table border="1">
<tr><th>Матч</th><th>Место</th><th>Цена</th><th>Дата продажи</th></tr>"""

    def _format_data(self, data: List[Dict[str, Any]]) -> str:
        rows = []
        for item in data:
            row = f"<tr><td>{item.get('match', '')}</td><td>{item.get('seat', '')}</td><td>{item.get('price', 0)} руб.</td><td>{item.get('sale_date', '')}</td></tr>"
            rows.append(row)
        return "\n".join(rows)

    def _add_footer(self) -> str:
        return f"""</table>
<p>Отчет сгенерирован: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</body>
</html>"""


class CSVReportGenerator(ReportGenerator):
    """Генератор отчета в формате CSV"""

    def _add_header(self) -> str:
        return "Матч,Место,Цена,Дата продажи"

    def _format_data(self, data: List[Dict[str, Any]]) -> str:
        rows = []
        for item in data:
            row = f"{item.get('match', '')},{item.get('seat', '')},{item.get('price', 0)},{item.get('sale_date', '')}"
            rows.append(row)
        return "\n".join(rows)

    def _add_footer(self) -> str:
        return f"# Отчет сгенерирован: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


class JSONReportGenerator(ReportGenerator):
    """Генератор отчета в формате JSON"""

    def _prepare_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Переопределяем подготовку данных для JSON формата.
        Добавляем метаинформацию.
        """
        prepared = super()._prepare_data(data)
        return prepared

    def _format_data(self, data: List[Dict[str, Any]]) -> str:
        report = {
            "report_type": "sales_report",
            "generated_at": datetime.now().isoformat(),
            "sales": data
        }
        return json.dumps(report, ensure_ascii=False, indent=2)

    def _add_header(self) -> str:
        # Для JSON заголовок не нужен
        return ""

    def _add_footer(self) -> str:
        # Для JSON подвал не нужен
        return ""


class ReportManager:
    """Управляет созданием отчетов с разными стратегиями форматирования"""

    def __init__(self, generator: ReportGenerator):
        self.generator = generator

    def set_generator(self, generator: ReportGenerator):
        """Смена генератора"""
        self.generator = generator

    def generate_report(self, data: List[Dict[str, Any]]) -> str:
        return self.generator.generate(data)


# 4. Демонстрация работы шаблонного метода
def demonstrate_template_method():
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНА «ШАБЛОННЫЙ МЕТОД»")
    print("=" * 60)

    # Тестовые данные о продажах
    sales_data = [
        {"match": "ЦСКА - Спартак", "seat": "Сектор A, 5-12", "price": 1500, "sale_date": "2026-03-15"},
        {"match": "ЦСКА - Спартак", "seat": "Сектор A, 5-13", "price": 1125, "sale_date": "2026-03-16"},
        {"match": "Зенит - Локомотив", "seat": "VIP Ложа, 3", "price": 4500, "sale_date": "2026-03-14"},
        {"match": "Динамо - Спартак", "seat": "Сектор B, 2-8", "price": 1200, "sale_date": "2026-03-17"},
    ]

    # Генерация отчета в разных форматах
    generators = [
        ("HTML", HTMLReportGenerator()),
        ("CSV", CSVReportGenerator()),
        ("JSON", JSONReportGenerator()),
    ]

    for format_name, generator in generators:
        print(f"\n--- ОТЧЕТ В ФОРМАТЕ {format_name} ---")
        report = generator.generate(sales_data)
        print(report)
        print("-" * 40)


if __name__ == "__main__":
    demonstrate_template_method()