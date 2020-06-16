import numpy as np
from datetime import datetime
import pandas as pd
import joblib

def outprint(stringx):
    print(stringx)
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    print(dt_string)

outprint("starting to read data finished")

#df = pd.read_csv("datasets/test-dataset.csv")
df = pd.read_csv("../openpowerlifting-2020-05-10.csv")


numrows = df.shape[0]
print(numrows)
