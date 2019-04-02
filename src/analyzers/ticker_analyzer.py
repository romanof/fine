import datetime

class TickerAnalyzer:

    def __init__(self, tickers):
        tickers.sort(key=lambda t: t.date)
        self.tickers = tickers

    def max(self, date, period_in_days, field):
        start_date = date - datetime.timedelta(days=period_in_days)
        if self.tickers[0].date > start_date: raise ValueError("invalid period")
        period_list = list(filter(lambda ticker: ticker.date >= start_date and ticker.date < date, self.tickers))
        return max(period_list, key=lambda ticker: getattr(ticker, field))

    def min(self, date, period_in_days, field):
        start_date = date - datetime.timedelta(days=period_in_days)
        if self.tickers[0].date > start_date: raise ValueError("invalid period")
        period_list = list(filter(lambda ticker: ticker.date >= start_date and ticker.date < date, self.tickers))
        return min(period_list, key=lambda ticker: getattr(ticker, field))

    def analyze(self, field, period, function):
        analysis = {}
        analysis["count"] = 0

        for idx, ticker in enumerate(self.tickers):
            try:
                func_ticker = getattr(self, function)(ticker.date, int(period), field)
                result = getattr(func_ticker, field)

                if ((function == "max" and getattr(ticker, field) > result) or
                    (function == "min" and getattr(ticker, field) < result)):

                    analysis["count"] += 1

                    for offset in [1, 3, 7, 14, 30]:
                        if not offset in analysis:
                            analysis[offset] = {}
                            analysis[offset]["sum_lo_percent_change"] = 0.0
                            analysis[offset]["sum_hi_percent_change"] = 0.0
                            analysis[offset]["lo_count"] = 0
                            analysis[offset]["hi_count"] = 0

                        change = (getattr(self.tickers[idx+offset], field) - result)
                        if getattr(self.tickers[idx+offset], field) >= result:
                            analysis[offset]["sum_hi_percent_change"] += change/result
                            analysis[offset]["hi_count"] += 1
                        else:
                            analysis[offset]["sum_lo_percent_change"] += change/result
                            analysis[offset]["lo_count"] += 1

            except (IndexError, ValueError):
                next

        return analysis
