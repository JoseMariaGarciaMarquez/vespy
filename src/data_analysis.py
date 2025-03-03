import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import t
from scipy.stats import chi2
from scipy.stats import f

class Analysis:
    def __init__(self, data):
        self.data = data