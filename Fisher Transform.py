import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/home/sirabas/Documents/Quant club/qn1 final/stock_prices.csv')
interval  = 9 #look back period

df['x'] = 0
df['fish'] = 0
df['fishwoema'] = 0
# I am using the Adj_Close values, we can use any other data also like (mean of high and low) or (just Close values)

# Initializing the first time-step variables
# Since I am using an ema of the values, we need previous data to compute current data.
# But for first element we are just using the calulated value instead of ema.

df.loc[interval,'x'] = 2*(df['Adj Close'].iloc[interval] - min(df['Adj Close'].iloc[0:interval]))/(max(df['Adj Close'].iloc[0:interval]) - min(df['Adj Close'].iloc[0:interval])) - 1
if(df.loc[interval,'x'] > 0.999):
   df.loc[interval,'x'] = 0.999
elif(df.loc[interval,'x'] < -0.999):
   df.loc[interval,'x'] = -0.999
df.loc[interval,'fish'] = 0.5*np.log((1+df.loc[interval,'x'])/(1-df.loc[interval,'x']))
df.loc[interval,'fishwoema'] = 0.5*np.log((1+df.loc[interval,'x'])/(1-df.loc[interval,'x']))

# Iterative calculation of values 
# using ema to smooth the fisher transform
# using ema with alpha = 0.5
# using ema for both x and fish values

for i in range(interval+1 , len(df['Adj Close'])):
    
   # We normalize the prices of previous interval data to (+1 , -1)
   # We then use ema
   # Then calculate the fisher transform values. 

   df.loc[i,'x'] = 0.5*2*(((df.loc[i,'Adj Close'] - min(df.loc[(i-interval):i,'Adj Close']))/(max(df.loc[(i-interval):i,'Adj Close']) - min(df.loc[(i-interval):i ,'Adj Close']))) - 0.5) + 0.5*df.loc[i-1,'x']
   
   if(df.loc[i,'x'] > 0.999):        # Some values may go above 1 as we are using ema of prev and curr
      df.loc[i,'x'] = 0.999          # So we are bounding them, so that fisher value doesn't blow up
   elif(df.loc[i,'x'] < -0.999):
      df.loc[i,'x'] = -0.999

   df.loc[i,'fishwoema'] = 0.5*np.log((1+df.loc[i,'x'])/(1-df.loc[i,'x']))
   df.loc[i,'fish'] = 0.25*np.log((1+df.loc[i,'x'])/(1-df.loc[i,'x'])) + 0.5*df.loc[i-1 ,'fish']


# We also plot a delayed FT to make predictions from cross-overs
df['fish_late'] = df['fish'].shift(1) 



fig , axis = plt.subplots(2,1)
axis[0].plot(df['Adj Close'] , label = 'price')
axis[1].plot(df['fish'] , label = 'fisher with ema')
axis[1].plot(df['fishwoema'] , label = 'fisher w/o ema')
#axis[1].plot(df['fish_late'] , label = 'delayed fish')
#df.to_csv('Fisher all data')
plt.legend()
plt.show()
