import pandas as pd
import matplotlib.pyplot as plt

from clean_crash_data import crash_data

glenway_data = crash_data[crash_data.STREET == 'GLENWAY AVE']