from polygon import RESTClient
import pandas as pd
from datetime import datetime, timedelta
import json

client = RESTClient()

tickers = ['BALL', 'CHTR', 'AES', 'CMCSA', 'CAG', 'CNC', 'LEN', 'DVN', 'PHM', 'HPQ']

data = []

for ticker in tickers:
    try:
        # Get current price
        snapshot = client.get_snapshot_all(market_type='stocks', tickers=[ticker])[0]
        price = snapshot.last_trade.price

        # Get 52w high
        from_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        to_date = datetime.now().strftime('%Y-%m-%d')
        aggs = client.get_aggs(ticker, 1, 'day', from_date, to_date)
        if not aggs:
            continue
        _52w_high = max(a.high for a in aggs)
        if _52w_high == 0:
            continue
        discount = 1 - price / _52w_high

        # Get TTM EPS
        financials = list(client.vx.list_stock_financials(ticker=ticker, timeframe='quarterly', limit=4))
        if len(financials) < 4:
            continue
        ttm_eps = sum(f.financials.income_statement.basic_earnings_per_share.value for f in financials)
        if ttm_eps <= 0:
            continue
        pe = price / ttm_eps

        # Get company name
        details = client.get_ticker_details(ticker)
        company = details.name

        data.append({
            'Ticker': ticker,
            'Company': company,
            'P/E Ratio': pe,
            'Discount from 52w High': discount
        })
    except Exception as e:
        continue

df = pd.DataFrame(data)
df = df.sort_values('P/E Ratio')

pareto = []
max_discount = -float('inf')
for index, row in df.iterrows():
    if row['Discount from 52w High'] > max_discount:
        pareto.append(row)
        max_discount = row['Discount from 52w High']

pareto_df = pd.DataFrame(pareto[:10])
pareto_df['Rank'] = range(1, len(pareto_df)+1)
pareto_df = pareto_df[['Rank', 'Company', 'Ticker', 'P/E Ratio', 'Discount from 52w High']]
pareto_df['P/E Ratio'] = pareto_df['P/E Ratio'].round(2)
pareto_df['Discount from 52w High'] = pareto_df['Discount from 52w High'].round(2)
print(pareto_df.to_markdown(index=False))

all_points = {
    'label': 'All Stocks',
    'data': [{'x': row['P/E Ratio'], 'y': row['Discount from 52w High'] } for index, row in df.iterrows()],
    'backgroundColor': 'rgba(0, 0, 255, 0.5)',
    'borderColor': 'blue'
}

pareto_points = {
    'label': 'Pareto Front',
    'data': [{'x': row['P/E Ratio'], 'y': row['Discount from 52w High'] } for index, row in pareto_df.iterrows()],
    'backgroundColor': 'rgba(255, 0, 0, 0.5)',
    'borderColor': 'red',
    'borderWidth': 1,
    'pointRadius': 5,
    'type': 'line'
}

chart_config = {
    'type': 'scatter',
    'data': {
        'datasets': [all_points, pareto_points]
    },
    'options': {
        'scales': {
            'x': {
                'type': 'linear',
                'position': 'bottom',
                'title': {'display': True, 'text': 'P/E Ratio'}
            },
            'y': {
                'type': 'linear',
                'title': {'display': True, 'text': 'Discount from 52w High'}
            }
        },
        'plugins': {
            'legend': {'display': True}
        }
    }
}

print(json.dumps(chart_config))

