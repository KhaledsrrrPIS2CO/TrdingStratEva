# Step 1: Get Data
# We’re going to use TLT as a proxy for bonds. We’ll use the yFinance library to get 10 years of data in 1 line of code.
#  But first, the imports:
import inline as inline
import matplotlib as matplotlib

#%matplotlib inline
import pandas as pd
import numpy as np

import yfinance as yf

tlt = yf.download("TLT", start="2002-01-01", end="2022-06-30")

# Step 2: Prepare Data
# Let’s add a few columns to the DataFrame that we’ll use later.
# First, we compute the log returns.

tlt["log_return"] = np.log(tlt["Adj Close"] / tlt["Adj Close"].shift(1))
#Then we’ll add a column for the calendar day of the month (1 – 31) and a column for the year.

tlt["day_of_month"] = tlt.index.day

tlt["year"] = tlt.index.year

# Step 3: Investigate Our Hypothesis

# We expect there to be positive returns in TLT toward the end of the month.
# We expect this because we think fund managers buy TLT at the end of the month.
# We expect there to be negative returns in TLT toward the beginning of the month.
# This is when fund managers sell their high-quality assets and go back to buying meme stocks.
# To see if this is true, we want the mean return on every day of the month.

grouped_by_day = tlt.groupby("day_of_month").log_return.mean()
# Then it’s simple to plot:

grouped_by_day.plot.bar(title="Mean Log Returns by Calendar Day of Month")

# Step 4: Build A Simple Trading Strategy
#Let’s build a naive strategy to test our hypothesis
# Buy and hold TLT during the last week of the month
# Short and hold TLT during the first week of the month

tlt["first_week_returns"] = 0.0
tlt.loc[tlt.day_of_month <= 7, "first_week_returns"] = tlt[
    tlt.day_of_month <= 7
].log_return

tlt["last_week_returns"] = 0.0
tlt.loc[tlt.day_of_month >= 23, "last_week_returns"] = tlt[
    tlt.day_of_month >= 23
].log_return

tlt["last_week_less_first_week"] = tlt.last_week_returns - tlt.first_week_returns

# Step 5: Plot Returns

(
    tlt.groupby("year")
    .last_week_less_first_week.mean()
    .plot.bar(title="Mean Log Strategy Returns by Year")
)

(
    tlt.groupby("year")
    .last_week_less_first_week.sum()
    .cumsum()
    .plot(title="Cumulative Sum of Returns By Year")
)

tlt.last_week_less_first_week.cumsum().plot(title="Cumulative Sum of Returns By Day")