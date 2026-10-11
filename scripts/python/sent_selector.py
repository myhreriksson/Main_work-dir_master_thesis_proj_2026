import argparse
import heapq
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--metric')
arg = parser.parse_args()

csv_file = 'results/coefficients/lmm_data.csv'

df = pd.read_csv(csv_file)