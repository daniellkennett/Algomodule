import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
fig = plt.figure()
#creating a subplot 
ax = fig.add_subplot(1,1,1)

def animate(i):
    data = pd.read_csv('../data/time_series_data.csv')
    xs = []
    ys = []
    values = data['5. Exchange Rate'].values
    for x,y in zip(range(len(values)), values):
        xs.append(x)
        ys.append(y)
    ax.clear()
    ax.plot(xs,ys)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('EUR/USD')
    fig.autofmt_xdate(rotation=45)

    
ani = FuncAnimation(fig, animate, interval=15000) 
plt.show()