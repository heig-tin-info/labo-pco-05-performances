import sys

import matplotlib.pyplot as plt
import pandas
import seaborn

frame = pandas.read_csv(sys.argv[1], names=["duration"])
q1 = frame["duration"].quantile(0.25)
q3 = frame["duration"].quantile(0.75)
iqr = q3 - q1

q1 = q1 - 1.5 * iqr
q3 = q3 + 1.5 * iqr

mask = frame["duration"].between(q1, q3, inclusive='both')
filtered = frame.loc[mask, "duration"]

ax = seaborn.histplot(filtered, kde=False)
ax.set(ylabel="Density", xlabel="Duration between slow iterations (ns)")
plt.show()