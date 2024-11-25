
# **Stock Portfolio Analyzer**
This Flask application allows users to manage a stock portfolio by adding stocks, calculating the portfolio value, and visualizing allocation and performance using Plotly charts. The app fetches stock data using Yahoo Finance and dynamically updates the portfolio metrics via a web interface.

---

## **Features**
1. **Add Stock to Portfolio**
   - Users can add a stock by providing the symbol and number of shares.
   - Fetches the latest price and historical data for the stock using the Yahoo Finance API.

2. **Portfolio Metrics Overview**
   - Displays the total portfolio value.
   - Visualizes the allocation of stocks in a pie chart.
   - Displays a line chart of portfolio performance over time.

3. **Interactive Web Interface**
   - Users interact with the application through a web-based interface with real-time updates.

---

## **Project Structure**
1. **Flask App**
   - Serves the web interface and provides backend routes for managing the portfolio.

2. **HTML Template**
   - Embedded HTML, CSS, and JavaScript for user interface and dynamic updates.

3. **Yahoo Finance Integration**
   - Fetches stock data (e.g., prices and historical performance) for analysis.

4. **Plotly Visualization**
   - Creates interactive pie and line charts for allocation and performance.

---

## **API Endpoints**

### **`GET /`**
- **Description**: Renders the main web interface for the Stock Portfolio Analyzer.
- **Response**: HTML page with input forms, portfolio metrics, and Plotly charts.

---

### **`POST /add_stock`**
- **Description**: Adds a stock to the portfolio.
- **Request Body**:
  - `symbol`: (String) Stock ticker symbol (e.g., `AAPL` for Apple).
  - `shares`: (Float) Number of shares to add.
- **Response**:
  - **Success**: JSON object with a success message.
  - **Failure**: JSON object with an error message (e.g., invalid stock symbol).

---

### **`GET /portfolio_metrics`**
- **Description**: Calculates portfolio metrics and prepares data for visualization.
- **Response**:
  - `portfolio_value`: (Float) Total value of the portfolio.
  - `allocation_data`: (JSON) Data for a pie chart showing stock allocation.
  - `performance_data`: (JSON) Data for a line chart showing portfolio performance over time.

---

## **HTML Template**

### **Dynamic Components**
1. **Stock Addition Form**:
   - Allows users to add stocks by specifying the symbol and number of shares.
2. **Portfolio Metrics**:
   - Displays total portfolio value dynamically.
3. **Allocation Pie Chart**:
   - Visualizes the percentage allocation of each stock.
4. **Performance Line Chart**:
   - Shows the portfolio's cumulative value over time.

### **JavaScript Features**
- **Fetch API**:
  - Sends requests to `/add_stock` and `/portfolio_metrics`.
- **Plotly Rendering**:
  - Dynamically updates pie and line charts based on server responses.

---

## **Backend Implementation**

### **Global Variables**
- `portfolio`: A dictionary storing stock data, including the number of shares, price, and historical data.

### **Core Logic**
1. **Adding Stocks**:
   - Fetches the latest price and 1-year historical data using `yfinance`.
   - Updates the `portfolio` dictionary with stock information.
2. **Portfolio Metrics Calculation**:
   - Computes total portfolio value and stock allocations.
   - Aggregates cumulative performance data over time.

---

## **Dependencies**
1. **Flask**: Web framework for routing and HTML rendering.
2. **Yahoo Finance (`yfinance`)**: Fetches stock data and historical prices.
3. **Pandas**: Processes and aggregates stock data.
4. **Plotly**: Generates interactive charts for visualization.
5. **JSON**: Encodes chart data for communication between backend and frontend.

---

## **Running the Application**

1. **Install Dependencies**:
   ```bash
   pip install flask yfinance pandas plotly
   ```
2. **Start the Server**:
   ```bash
   python app.py
   ```
3. **Access the Application**:
   - Open a browser and navigate to `http://127.0.0.1:5000`.

---

## **Example Usage**
1. Launch the application.
2. Add stocks using their ticker symbols and number of shares.
3. View updated portfolio metrics, allocation chart, and performance chart.

---
