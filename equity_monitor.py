import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

class EquityMonitor:
    def __init__(self, symbols):
        self.symbols = symbols
        self.df = pd.DataFrame()
        self.market_data = None
        self._fetch_market_data()

    def _fetch_market_data(self):
        """Fetches market data once to be used for Beta calculation."""
        try:
            merval = yf.Ticker("^MERV")
            self.market_data = merval.history(period="1y")
        except Exception as e:
            print(f"Error fetching market data: {e}")
            self.market_data = None

    def get_stock_data(self, symbol):
        """
        Obtains stock data from Yahoo Finance including industry info, technicals, and fundamentals.
        """
        try:
            # Create ticker object
            ticker = yf.Ticker(symbol)

            # Get general info
            info = ticker.info

            # Get historical data (1 year for trend analysis)
            hist = ticker.history(period="1y")

            if hist.empty:
                return None

            # Current price
            current_price = hist['Close'].iloc[-1]

            # --- Variations ---
            var_1w = self._calculate_variation(hist, 7)
            var_1m = self._calculate_variation(hist, 30)
            var_1y = self._calculate_variation(hist, 365, from_start=True)
            var_ytd = self._calculate_ytd(ticker, current_price)

            # --- Technical Indicators ---
            rsi = self._calculate_rsi(hist)
            sma_200 = self._calculate_sma(hist, 200)
            price_vs_sma200 = (current_price / sma_200 - 1) * 100 if sma_200 else None

            # --- Beta ---
            beta = self._calculate_beta(hist)

            # --- Fundamentals ---
            market_cap = info.get('marketCap')
            ev = info.get('enterpriseValue')
            ev_ebitda = info.get('enterpriseToEbitda')
            pe_ratio = info.get('trailingPE')
            price_to_sales = info.get('priceToSalesTrailing12Months')
            price_to_book = info.get('priceToBook')
            profit_margin = info.get('profitMargins')
            roe = info.get('returnOnEquity')
            avg_volume = info.get('averageVolume')

            # --- Scoring ---
            score = self._calculate_score(pe_ratio, ev_ebitda, roe, profit_margin, price_vs_sma200, rsi)

            return {
                'Symbol': symbol.replace('.BA', ''),
                'Company': info.get('shortName', symbol.replace('.BA', '')),
                'Sector': info.get('sector', 'N/A'),
                'Industry': info.get('industry', 'N/A'),
                'Price': current_price,
                'Var 1W (%)': var_1w,
                'Var 1M (%)': var_1m,
                'Var 1Y (%)': var_1y,
                'Var YTD (%)': var_ytd,
                'RSI': rsi,
                'Price vs SMA200 (%)': price_vs_sma200,
                'Beta': beta,
                'Market Cap': market_cap,
                'EV': ev,
                'EV/EBITDA': ev_ebitda,
                'P/E': pe_ratio,
                'P/S': price_to_sales,
                'P/B': price_to_book,
                'Margin (%)': profit_margin * 100 if profit_margin else None,
                'ROE (%)': roe * 100 if roe else None,
                'Avg Volume': avg_volume,
                'Score': score
            }

        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            return None

    def _calculate_variation(self, hist, days, from_start=False):
        try:
            current_price = hist['Close'].iloc[-1]
            if from_start:
                 ref_price = hist['Close'].iloc[0]
            else:
                 # Check if we have enough data
                 if len(hist) < days:
                     return None
                 # Approximate trading days (5 days a week)
                 lookback = int(days * 5/7)
                 if lookback >= len(hist):
                     lookback = len(hist) - 1
                 ref_price = hist['Close'].iloc[-lookback]

            return ((current_price - ref_price) / ref_price) * 100
        except:
            return None

    def _calculate_ytd(self, ticker, current_price):
        try:
            start_of_year = datetime(datetime.now().year, 1, 1)
            ytd_hist = ticker.history(start=start_of_year)
            if not ytd_hist.empty:
                first_day_price = ytd_hist['Close'].iloc[0]
                return ((current_price - first_day_price) / first_day_price) * 100
        except:
            pass
        return None

    def _calculate_beta(self, hist):
        try:
            if self.market_data is None or self.market_data.empty:
                return None

            # Align dates
            stock_rets = hist['Close'].pct_change().dropna()
            mkt_rets = self.market_data['Close'].pct_change().dropna()

            # Inner join on index (Date)
            common_dates = stock_rets.index.intersection(mkt_rets.index)
            stock_rets = stock_rets.loc[common_dates]
            mkt_rets = mkt_rets.loc[common_dates]

            if len(stock_rets) > 30:
                cov_matrix = np.cov(stock_rets, mkt_rets)
                covariance = cov_matrix[0][1]
                variance = cov_matrix[1][1]
                if variance != 0:
                    return covariance / variance
        except:
            pass
        return None

    def _calculate_rsi(self, hist, window=14):
        try:
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs)).iloc[-1]
        except:
            return None

    def _calculate_sma(self, hist, window=200):
        try:
            if len(hist) < window:
                return None
            return hist['Close'].rolling(window=window).mean().iloc[-1]
        except:
            return None

    def _calculate_score(self, pe, ev_ebitda, roe, margin, price_sma, rsi):
        """
        Calculates a score from 0 to 100 based on Value, Quality, and Momentum.
        """
        score = 0
        count = 0

        # --- Value (Lower is better) ---
        if pe:
            if 0 < pe < 10: score += 10
            elif 10 <= pe < 20: score += 7
            elif 20 <= pe < 30: score += 4
            count += 1 # Weight 1

        if ev_ebitda:
            if 0 < ev_ebitda < 8: score += 10
            elif 8 <= ev_ebitda < 15: score += 7
            elif 15 <= ev_ebitda < 25: score += 4
            count += 1

        # --- Quality (Higher is better) ---
        if roe:
            if roe > 0.20: score += 10
            elif roe > 0.10: score += 7
            elif roe > 0.05: score += 4
            count += 1

        if margin:
            if margin > 0.15: score += 10
            elif margin > 0.08: score += 7
            elif margin > 0: score += 4
            count += 1

        # --- Momentum ---
        if price_sma is not None:
            if price_sma > 0: score += 10 # Above SMA 200 (Bullish trend)
            elif price_sma > -10: score += 5
            count += 1

        if rsi is not None:
            if 40 <= rsi <= 70: score += 10 # Healthy zone
            elif rsi > 70: score += 5 # Overbought but strong
            elif rsi < 30: score += 2 # Oversold
            count += 1

        # Normalize to 100
        # Max points per item is 10. Max total items is 6. Max score = 60.
        # We want to scale it to 100.
        if count > 0:
            final_score = (score / (count * 10)) * 100
            return round(final_score, 1)
        return 0

    def run_analysis(self):
        print(f"Starting analysis for {len(self.symbols)} symbols...")
        data = []
        for symbol in self.symbols:
            print(f"Fetching {symbol}...", end="\r")
            stock_data = self.get_stock_data(symbol)
            if stock_data:
                data.append(stock_data)

        print("\nAnalysis complete.")
        self.df = pd.DataFrame(data)

        # Sort by Industry and Score
        if not self.df.empty:
            self.df = self.df.sort_values(['Industry', 'Score'], ascending=[True, False]).reset_index(drop=True)

        return self.df

    def format_large_numbers(self, value):
        if isinstance(value, (int, float)):
            if value >= 1e9: return f"{value/1e9:.1f}B"
            if value >= 1e6: return f"{value/1e6:.1f}M"
            if value >= 1e3: return f"{value/1e3:.1f}K"
            return f"{value:.2f}"
        return value

    def display_report(self):
        if self.df.empty:
            print("No data available.")
            return

        # Create a display copy to format numbers
        display_df = self.df.copy()

        # Format columns
        large_num_cols = ['Market Cap', 'EV', 'Avg Volume']
        for col in large_num_cols:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(self.format_large_numbers)

        pct_cols = ['Var 1W (%)', 'Var 1M (%)', 'Var 1Y (%)', 'Var YTD (%)', 'Price vs SMA200 (%)', 'Margin (%)', 'ROE (%)']
        for col in pct_cols:
             if col in display_df.columns:
                 display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "-")

        float_cols = ['Price', 'RSI', 'Beta', 'EV/EBITDA', 'P/E', 'P/S', 'P/B', 'Score']
        for col in float_cols:
             if col in display_df.columns:
                 display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "-")

        # Columns to show
        cols = ['Symbol', 'Sector', 'Industry', 'Price', 'Score', 'RSI', 'Var YTD (%)', 'P/E', 'EV/EBITDA', 'ROE (%)']
        print(display_df[cols].to_string(index=False))

    def to_csv(self, filename="equity_report.csv"):
        self.df.to_csv(filename, index=False)
        print(f"Report saved to {filename}")

if __name__ == "__main__":
    # Test run
    symbols = ['GGAL.BA', 'YPFD.BA', 'PAMP.BA']
    monitor = EquityMonitor(symbols)
    df = monitor.run_analysis()
    monitor.display_report()
