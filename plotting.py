import matplotlib.pyplot as plt
from stock import Stock
import plotly.graph_objects as go


def get_stock_chart(stock):
    if stock.data is None or stock.data.empty:
        print(f"No data available for {stock.ticker}")
        return
    if stock.data.empty:
        print(f"Cannot plot {stock.ticker}: no data")
        return
    if "Close" not in stock.data.columns:
        print(f"Cannot plot {stock.ticker}: 'Close' column missing")
        return
    plt.figure(figsize=(10,5))
    plt.plot(stock.data.index, stock.data["Close"], label=stock.ticker)
    plt.title(f"{stock.ticker} Historical Price")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid(True)
    plt.show()


def compare_charts_interactive_enhanced(stocks):
    fig = go.Figure()
    summary = []

    for stock in stocks:
        if stock.data is None or stock.data.empty or "Close" not in stock.data.columns:
            print(f"Skipping {stock.ticker}: No valid 'Close' data.")
            continue

        df = stock.data.copy()
        pct_return = ((df["Close"] - df["Close"].iloc[0]) / df["Close"].iloc[0]) * 100

        fig.add_trace(go.Scatter(
            x=df.index,
            y=pct_return,
            mode='lines',
            name=stock.ticker,
            line=dict(width=2),
            hovertemplate=(
                f"<b>{stock.ticker}</b><br>" +
                "Date: %{x|%Y-%m-%d}<br>" +
                "Return: %{y:.2f}%<br>" +
                "Open: %{customdata[0]:.2f}<br>" +
                "High: %{customdata[1]:.2f}<br>" +
                "Low: %{customdata[2]:.2f}<br>" +
                "Volume: %{customdata[3]:,}<extra></extra>"
            ),
            customdata=df[["Open", "High", "Low", "Volume"]].values
        ))

        start_price = df["Close"].iloc[0]
        end_price = df["Close"].iloc[-1]
        total_return = ((end_price - start_price) / start_price) * 100
        summary.append((stock.ticker, round(start_price, 2), round(end_price, 2), round(total_return, 2)))

    fig.update_layout(
        title="📊 Interactive Stock Growth Comparison",
        xaxis_title="Date",
        yaxis_title=f"Return Since {stocks[0].data.index[0].strftime('%Y-%m-%d')} (%)",
        legend_title="Stock Ticker",
        template="plotly_white",
        hovermode="x unified",
        width=1000,
        height=600,
        xaxis=dict(
            showgrid=True, 
            gridcolor='lightgray',
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )

    fig.show()

    print("\n📈 Stock Performance Summary:")
    print("-" * 60)
    for ticker, start, end, change in summary:
        direction = "▲" if change > 0 else "▼" if change < 0 else "→"
        print(f"{ticker}: {direction} {change:+.2f}%  (from ${start} to ${end})")
    print("-" * 60)
