"# Donchian-Channel-Trading" 

Introduction

The Donchian channel is a simple trend following technique for financial trading.  The channel is defined by the max and min prices the financial product traded at for the specified days in the past, e.g. 50 days.  The basic intuition is to trade on the side of the breakouts from the window as the move signifies a potential trend about to occur or already underway.  While a breakout does not suffice to guarantee a trend in the future, a breakout is the necessary condition to the future trend.  By adding to the position on the side of the breakout, it is hoped that the trader will be on the trend when it does occur.

A naive Dochian channel's implementation, i.e. commmitting all capital in position when breakout is identified, tends to lead to large volatilities in the portfolio.  This is easy natural as many breakouts turn out false, and the damage done by the false signals impacts the portfolio's performance.


