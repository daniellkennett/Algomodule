import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
fig = plt.figure()
#creating a subplot 
ax = fig.add_subplot(1,1,1)

def historic_animate(i, file = 'historic_time_series_data.csv'):
    data = pd.read_csv(f'../data/{file}')
    xs = []
    ys = []
    values = data['4. close'].values
    ax.plot(values,range(len(values)))
    for x,y in zip(range(len(values)), values):
        xs.append(x)
        ys.append(y)

    ax.plot(xs,ys)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('EUR/USD')
    fig.autofmt_xdate(rotation=45)

    
ani = FuncAnimation(fig, historic_animate, interval=100) 
plt.show()
