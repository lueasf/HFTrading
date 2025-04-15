#!/usr/bin/env python3
import unittest
import pytest
import sys
import os

if __name__ == "__main__":
    """
    Run unit tests for the backtest framework.
    
    Usage:
    - Run all tests: python run_tests.py
    - Run specific test file: python run_tests.py test_orderbook
    - Run specific test class: python run_tests.py test_orderbook.TestOrderBook
    - Run specific test method: python run_tests.py test_orderbook.TestOrderBook.test_add_bid
    """
    # Add the project root to path to ensure imports work
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        # If it's a file name without extension, add .py
        if '.' not in test_name and not test_name.startswith('test_'):
            test_name = f'test_{test_name}.py'
        elif '.' not in test_name and test_name.startswith('test_'):
            test_name = f'{test_name}.py'
        
        # Run with pytest for better output
        pytest.main([f'tests/{test_name}', '-v'])
    else:
        # Discover and run all tests
        test_suite = unittest.defaultTestLoader.discover('tests')
        test_runner = unittest.TextTestRunner(verbosity=2)
        test_runner.run(test_suite)