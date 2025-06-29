import unittest
from dao.tax_service import TaxService
from exceptions.custom_exceptions import TaxCalculationException

class TestTaxCalculation(unittest.TestCase):
    def setUp(self):
        self.tax_service = TaxService()

    def test_zero_tax(self):
        """Income <= 300000 should return 0 tax"""
        self.assertEqual(self.tax_service.calculate_tax(200000), 0)

    def test_low_slab_tax(self):
        """Income = 400000 -> (400000 - 300000) * 5% = 5000"""
        self.assertAlmostEqual(self.tax_service.calculate_tax(400000), 5000.0)

    def test_middle_slab_tax(self):
        """Income = 700000
        Tax = 300000*5% + (700000 - 600000)*10% = 15000 + 10000 = 25000"""
        self.assertAlmostEqual(self.tax_service.calculate_tax(700000), 25000.0)

    def test_high_slab_tax(self):
        """Income = 1200000
        Tax = 300000*5% + 300000*10% + (1200000 - 900000)*15%
            = 15000 + 30000 + 45000 = 90000"""
        self.assertAlmostEqual(self.tax_service.calculate_tax(1200000), 90000.0)

    def test_negative_income(self):
        """Negative income should raise a TaxCalculationException"""
        with self.assertRaises(TaxCalculationException):
            self.tax_service.calculate_tax(-50000)

if __name__ == '__main__':
    unittest.main()
