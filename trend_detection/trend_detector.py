import numpy as np
import pymannkendall as mk


def trend_detector(data):
    return mk.original_test(data)
