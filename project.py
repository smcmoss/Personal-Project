from flask import Flask, render_template_string, request, jsonify
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.utils  # Required for JSON serialization of Plotly objects
import json

app = Flask(__name__)

# Initialize an empty portfolio dictionary
portfolio = {}

# HTML template with embedded CSS and JavaScript for Plotly charts
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Stock Portfolio Analyzer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }
        form, h2 {
            margin-top: 20px;
        }
        #portfolio-value {
            font-weight: bold;
            margin-top: 20px;
        }
        #allocation-chart, #performance-chart {
            width: 80%;
            margin: auto;
            margin-top: 20px;
        }
    </style>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Stock Portfolio Analyzer</h1>
    
    <h2>Add Stock</h2>
    <form id="add-stock-form">
        <label for="symbol">Stock Symbol:</label>
        <input type="text" id="symbol" name="symbol" required>
        <label for="shares">Shares:</label>
        <input type="number" step="0.01" id="shares" name="shares" required>
        <button type="submit">Add Stock</button>
    </form>

    <h2>Portfolio Overview</h2>
    <div id="portfolio-value"></div>
    <div id="allocation-chart"></div>
    <div id="performance-chart"></div>

    <script>
        // Handle stock addition form
        document.getElementById('add-stock-form').onsubmit = function(event) {
            event.preventDefault();
            const symbol = document.getElementById('symbol').value;
            const shares = document.getElementById('shares').value;

            fetch('/add_stock', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symbol: symbol, shares: shares })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                loadPortfolioMetrics(); // Refresh portfolio data after adding a stock
            })
            .catch(error => console.error('Error:', error));
        };

        // Fetch and display portfolio metrics and performance
        function loadPortfolioMetrics() {
            fetch('/portfolio_metrics')
            .then(response => response.json())
            .then(data => {
                document.getElementById('portfolio-value').innerText = `Portfolio Value: $${data.portfolio_value.toFixed(2)}`;

                // Render allocation chart
                Plotly.newPlot('allocation-chart', data.allocation_data, { title: "Portfolio Allocation" });

                // Render performance chart
                Plotly.newPlot('performance-chart', data.performance_data, { title: "Portfolio Performance Over Time" });
            })
            .catch(error => console.error('Error:', error));
        }

        // Refresh portfolio metrics on load
        window.onload = loadPortfolioMetrics;
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

# Route to add a stock to the portfolio
@app.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.get_json()
    stock_symbol = data['symbol'].upper()
    shares = float(data['shares'])

    try:
        # Fetch stock data
        stock_data = yf.Ticker(stock_symbol)
        hist_data = stock_data.history(period="1y")  # 1-year historical data

        if hist_data.empty:
            return jsonify({"message": f"Stock symbol '{stock_symbol}' not found."}), 400
        
        latest_price = hist_data['Close'].iloc[-1]

        # Add stock to portfolio
        if stock_symbol in portfolio:
            portfolio[stock_symbol]['shares'] += shares
        else:
            portfolio[stock_symbol] = {'shares': shares, 'price': latest_price, 'data': hist_data}

        return jsonify({"message": f"Added {shares} shares of {stock_symbol} at ${latest_price:.2f} each."})

    except Exception as e:
        return jsonify({"message": f"Error fetching data for {stock_symbol}: {str(e)}"}), 500

# Route to calculate and display portfolio metrics and performance
@app.route('/portfolio_metrics')
def portfolio_metrics():
    portfolio_value = 0
    allocations = {}
    cumulative_value = pd.DataFrame()  # DataFrame to store cumulative values

    for symbol, info in portfolio.items():
        stock_value = info['shares'] * info['price']
        portfolio_value += stock_value
        allocations[symbol] = stock_value

        # Calculate cumulative value over time for each stock
        stock_cumulative = info['data']['Close'] * info['shares']
        cumulative_value[symbol] = stock_cumulative

    if portfolio_value == 0:
        return jsonify({"message": "Portfolio is empty or all stocks have zero value."}), 400

    # Calculate allocation percentages
    allocations = {symbol: (value / portfolio_value) * 100 for symbol, value in allocations.items()}

    # Prepare data for allocation pie chart
    allocation_data = [go.Pie(labels=list(allocations.keys()), values=list(allocations.values()))]

    # Calculate total portfolio value over time
    cumulative_value['Total'] = cumulative_value.sum(axis=1)

    # Prepare portfolio performance line chart
    performance_data = [go.Scatter(x=cumulative_value.index, y=cumulative_value['Total'], mode='lines', name='Portfolio Value')]

    # Encode charts data in JSON format
    allocation_data_json = json.loads(json.dumps(allocation_data, cls=plotly.utils.PlotlyJSONEncoder))
    performance_data_json = json.loads(json.dumps(performance_data, cls=plotly.utils.PlotlyJSONEncoder))

    return jsonify({
        "portfolio_value": portfolio_value,
        "allocation_data": allocation_data_json,
        "performance_data": performance_data_json
    })

if __name__ == '__main__':
    app.run(debug=True)