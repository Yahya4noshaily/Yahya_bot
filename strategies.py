import numpy as np

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100. / (1. + rs)

    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            up_val = delta
            down_val = 0.
        else:
            up_val = 0.
            down_val = -delta

        up = (up * (period - 1) + up_val) / period
        down = (down * (period - 1) + down_val) / period

        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi

def rsi_strategy(prices, period=14, overbought=70, oversold=30):
    rsi = calculate_rsi(prices, period)
    last_rsi = rsi[-1]

    if last_rsi > overbought:
        return "بيع (SELL)"
    elif last_rsi < oversold:
        return "شراء (BUY)"
    else:
        return "انتظار"

def calculate_macd(prices, slow=26, fast=12, signal=9):
    exp1 = exponential_moving_average(prices, fast)
    exp2 = exponential_moving_average(prices, slow)
    macd = exp1 - exp2
    signal_line = exponential_moving_average(macd, signal)
    histogram = macd - signal_line
    return macd, signal_line, histogram

def exponential_moving_average(prices, period):
    ema = np.zeros_like(prices)
    alpha = 2 / (period + 1)
    ema[0] = prices[0]
    for i in range(1, len(prices)):
        ema[i] = alpha * prices[i] + (1 - alpha) * ema[i - 1]
    return ema

def macd_strategy(prices):
    macd, signal_line, histogram = calculate_macd(prices)
    if macd[-1] > signal_line[-1] and histogram[-1] > 0:
        return "شراء (BUY)"
    elif macd[-1] < signal_line[-1] and histogram[-1] < 0:
        return "بيع (SELL)"
    else:
        return "انتظار"

def moving_average_strategy(prices, short_period=5, long_period=20):
    short_ma = simple_moving_average(prices, short_period)
    long_ma = simple_moving_average(prices, long_period)

    if short_ma[-1] > long_ma[-1]:
        return "شراء (BUY)"
    elif short_ma[-1] < long_ma[-1]:
        return "بيع (SELL)"
    else:
        return "انتظار"

def simple_moving_average(prices, period):
    sma = np.convolve(prices, np.ones(period)/period, mode='valid')
    return np.concatenate((np.zeros(period-1), sma))

def combined_strategy(prices):
    signals = []
    signals.append(rsi_strategy(prices))
    signals.append(macd_strategy(prices))
    signals.append(moving_average_strategy(prices))

    buy_signals = signals.count("شراء (BUY)")
    sell_signals = signals.count("بيع (SELL)")

    if buy_signals > sell_signals:
        return "شراء (BUY)"
    elif sell_signals > buy_signals:
        return "بيع (SELL)"
    else:
        return "انتظار"
