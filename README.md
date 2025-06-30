## STOCK TRACKER PORTFOLIO
This is a Django-based web application that allows users to manage and track their stock investments with real-time market price updates and automated profit/loss analysis. It leverages live data via Yahoo Finance (`yfinance`), logs actions using MongoDB, and is optionally compatible with Power BI for extended analytics.

---
![Screenshot 2025-06-30 193630](https://github.com/user-attachments/assets/b363a1c4-c0a3-4f31-9c9a-2f1c9f8644fe)
![Screenshot 2025-06-30 193645](https://github.com/user-attachments/assets/ff82d7b0-03d7-41dd-b460-4700ac50984c)
![Screenshot 2025-06-30 193700](https://github.com/user-attachments/assets/d458b618-13bc-4334-b277-3bf1135f8bc0)




## Features

- Add and manage stock holdings per user
- Real-time stock price fetching using `yfinance`
- Profit/Loss calculated based on the actual buy price at the time of entry
- Investment value remains static (does not change with daily market fluctuations)
- Clickable stock tickers to view recent price trends (up/down/no change)
- User-wise portfolio summaries with total investment, current value, and profit/loss
- Backend logging using MongoDB
- Responsive and clean user interface built with Bootstrap 5

---

## Technology Stack

| Layer           | Technologies                          |
|----------------|----------------------------------------|
| Backend         | Django, Python, SQLite |
| Frontend        | HTML, CSS (Bootstrap 5)   |
| Realtime Data   | Yahoo Finance via `yfinance`           |
| Logging         | MongoDB using `pymongo`                |
| Caching         | Django cache framework (in-memory or file-based) |

---

## Setup Instructions

1. **Clone or extract the project**
   - If uploading as a `.zip`, extract the folder
   - If using Git:
     ```bash
     git clone https://github.com/stock-portfolio-tracker.git
     cd stock-portfolio-tracker
     ```

2. **Create a virtual environment and activate it**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
