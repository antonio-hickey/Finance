//@version=4
//------------------------------------------------------------------------------
// © Antonio Hickey --------------------------------------------------------------
// Fianchetto v1 ---------------------------------------------------------------
// **Optimized For Currency Trading** ------------------------------------------
//------------------------------------------------------------------------------
// Defining strategy and settings
//------------------------------------------------------------------------------
strategy(title="Fianchetto v1", overlay=true, pyramiding=0, initial_capital=5000, currency=currency.USD, calc_on_order_fills=0, default_qty_type=strategy.fixed, default_qty_value=4)
//------------------------------------------------------------------------------
// Timeframe for backtest
//------------------------------------------------------------------------------
testStartYear = input(2016, "Backtest Start Year")
testStartMonth = input(9, "Backtest Start Month")
testStartDay = input(30, "Backtest Start Day")
testPeriodStart = timestamp(testStartYear,testStartMonth,testStartDay, 0, 0)

testStopYear = input(2018, "Backtest Stop Year")
testStopMonth = input(1, "Backtest Stop Month")
testStopDay = input(10, "Backtest Stop Day")
testPeriodStop = timestamp(testStopYear,testStopMonth,testStopDay, 0, 0)

testPeriod() => time >= testPeriodStart and time <= testPeriodStop ? true : false
//------------------------------------------------------------------------------
// Inputs
//------------------------------------------------------------------------------
Baseline_MA_Len = input(200,"Baseline MA")
Attack_MA_Len = input(7,"Attack MA") 
source = input(close,"Source")
Baseline_Filter = input(true,"Use Baseline only as filter?")
vFactor = input(0.7,"volume factor (between 0-1)",minval=0, maxval=1)
exit_Rev = input(true,"Use Attacks for exit signal")
//------------------------------------------------------------------------------
// Triple EMA
//------------------------------------------------------------------------------
rev_funct(src, length) =>
    ema(src, length) * (1+vFactor) - ema(ema(src, length), length) * vFactor

rev = rev_funct(rev_funct(rev_funct(source, Attack_MA_Len), Attack_MA_Len), Attack_MA_Len)
//------------------------------------------------------------------------------
// Conditions
//------------------------------------------------------------------------------
Bull_Attack = Baseline_Filter?(rev > rev[1] and close>sma(close, Baseline_MA_Len)) :crossover(rev, sma(close, Baseline_MA_Len))
exitbuys = rev < rev[1]
 
Bear_Attack = Baseline_Filter?(rev < rev[1] and close<sma(close, Baseline_MA_Len)) :crossunder(rev, sma(close, Baseline_MA_Len))
exitsells = rev > rev[1]
//------------------------------------------------------------------------------
// Trading Logic
if (Bull_Attack and testPeriod()) 
    strategy.entry("BUY", strategy.long)
strategy.close("BUY", when = exitbuys and exit_Rev)

if (Bear_Attack and testPeriod())
    strategy.entry("SELL", strategy.short)
strategy.close("SELL", when = exitsells and exit_Rev)
//------------------------------------------------------------------------------
// Plotting
//------------------------------------------------------------------------------
plot(sma(close, Baseline_MA_Len),"SMA",color.orange)
plot(rev,"rev",rev > rev[1] ? color.green : color.red)
//------------------------------------------------------------------------------
//© Antonio Hickey --------------------------------------------------------------
//END---------------------------------------------------------------------------
