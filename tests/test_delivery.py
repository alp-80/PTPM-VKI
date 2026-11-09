import unittest
import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.delivery_service import calculate_delivery_cost

FIXED_TODAY = "2026-09-03"


class TestDeliveryValidation(unittest.TestCase):

    def test_weight_below_minimum_returns_error(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_above_maximum_returns_error(self):
        cost, date = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_above_maximum_returns_error(self):
        cost, date = calculate_delivery_cost(1.0, 5001, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_unknown_package_type_returns_error(self):
        cost, date = calculate_delivery_cost(1.0, 100, "неизвестный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")
        
    def test_unknown_package_type_returns_error2(self):
        cost, date = calculate_delivery_cost(70.0, 600, "опасный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")


class TestDeliveryCostCalculation(unittest.TestCase):

    def test_basic_cost_formula(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_medium_weight_applies_1_2_coefficient(self):
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_heavy_weight_applies_1_5_coefficient(self):
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_fragile_package_adds_300(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_package_adds_1000(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)


class TestExpressDelivery(unittest.TestCase):

    def test_express_costs_more_than_regular(self):
        regular, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=False)
        express, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertGreater(express, regular, "экспресс доставка должна стоить дороже обычной")

    def test_express_never_delivers_same_day(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertNotEqual(date, FIXED_TODAY, "экспресс не должен доставляться в день отправки")


class TestDeliveryDates(unittest.TestCase):

    def test_date_scales_with_distance(self):
        _, date = calculate_delivery_cost(1.0, 2000, "обычный")
        self.assertEqual(date, "2026-09-07")

    def test_date_format_is_iso(self):
        _, date = calculate_delivery_cost(1.0, 1000, "обычный")
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")


if __name__ == "__main__":
    unittest.main()