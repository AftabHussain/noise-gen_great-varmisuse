import pandas as pd

df = pd.read_csv('log_train_len.txt')

import matplotlib.pyplot as plt

data = df['#num_of_rep_cands']
print(data.max())

fig = data.plot(kind='hist')


# Bins using binwidth
# Ref: https://stackoverflow.com/questions/6986986/bin-size-in-matplotlib-histogram
#binwidth = 10
#plt.hist(data, bins=range(min(data), max(data) + binwidth, binwidth))

# Ref: https://towardsdatascience.com/histograms-with-pythons-matplotlib-b8b768da9305
n, bins, patches = plt.hist(data)
bins_int = bins.astype(int)
plt.xticks(bins_int)
xticks = [(bins[idx+1] + value)/2 for idx, value in enumerate(bins[:-1])]
for idx, value in enumerate(n):
    if value > 0:
        plt.text(xticks[idx], value+5, int(value), ha='center')


plt.xlabel('Source Token Length')
plt.savefig('test.png')
