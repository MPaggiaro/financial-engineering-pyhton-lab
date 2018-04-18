from unittest import TestCase
import numpy as np
import solutions

class EuropeanOption:
    strike = 1.0
    spot_price = 1.0
    time_to_maturity = 1.0
    volatility = 0.20
    zero_rate = 0.03
    dividends = 0.0
    

class EuropeanOptionMCTest(TestCase):
    
    def __init__(self, testname, student_function):
        super(EuropeanOptionMCTest, self).__init__(testname)
        self.student_function = student_function
    
    def test_call(self):
        option = EuropeanOption()
        discount_factor = np.exp(-option.zero_rate*option.time_to_maturity)
        forward = option.spot_price/discount_factor
        number_of_samples = 1000
        np.random.seed(218423)
        expected_price = solutions.EuropeanOptionMC(forward, option.strike, discount_factor, option.time_to_maturity, option.volatility, number_of_samples, 1)
        np.random.seed(218423)
        actual_price = self.student_function(forward, option.strike, discount_factor, option.time_to_maturity, option.volatility, number_of_samples, 1)
        self.assertAlmostEqual(expected_price, actual_price)
        
    def test_put(self):
        option = EuropeanOption()
        discount_factor = np.exp(-option.zero_rate*option.time_to_maturity)
        forward = option.spot_price/discount_factor
        number_of_samples = 1000
        np.random.seed(218423)
        expected_price = solutions.EuropeanOptionMC(forward, option.strike, discount_factor, option.time_to_maturity, option.volatility, number_of_samples, -1)
        np.random.seed(218423)
        actual_price = self.student_function(forward, option.strike, discount_factor, option.time_to_maturity, option.volatility, number_of_samples, -1)
        self.assertAlmostEqual(expected_price, actual_price)
        

class ReadSwapRatesTest(TestCase):

    file = 'MktData_CurveBootstrap.xls'
    sheet = 'Data'
    fromRow = 37
    columnRange = 'D:F'
    
    def __init__(self, testname, student_function):
        super(ReadSwapRatesTest, self).__init__(testname)
        self.student_function = student_function
        self.expected_data_frame = solutions.ReadSwapRates(self.file, self.sheet, self.fromRow, self.columnRange)

    def test_header(self):
        actual_data_frame = self.student_function(self.file, self.sheet, self.fromRow, self.columnRange)
        self.assertEqual(self.expected_data_frame.columns.tolist(), actual_data_frame.columns.tolist())

    def test_number_of_rows(self):
        actual_data_frame = self.student_function(self.file, self.sheet, self.fromRow, self.columnRange)
        self.assertEqual(self.expected_data_frame.shape[0], actual_data_frame.shape[0])

    def test_dates(self):
        actual_data_frame = self.student_function(self.file, self.sheet, self.fromRow, self.columnRange)
        self.assertEqual(self.expected_data_frame.ix[:,0].tolist(), actual_data_frame.ix[:,0].tolist())

    def test_bids(self):
        actual_data_frame = self.student_function(self.file, self.sheet, self.fromRow, self.columnRange)
        self.assertEqual(self.expected_data_frame.ix[:,1].tolist(), actual_data_frame.ix[:,1].tolist())

    def test_asks(self):
        actual_data_frame = self.student_function(self.file, self.sheet, self.fromRow, self.columnRange)
        self.assertEqual(self.expected_data_frame.ix[:,2].tolist(), actual_data_frame.ix[:,2].tolist())