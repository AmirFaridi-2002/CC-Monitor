# Cryptocurrency Price Tracker

This Python project monitors the prices of multiple cryptocurrencies and sends alerts through a Telegram bot when a specific price pattern is met. The project also generates charts for analysis and provides them to authorized admins.

## Features

- **Multi-Currency Tracking**: Uses `threading` to monitor several cryptocurrencies simultaneously.
- **Pattern-Based Alerts**: Sends alerts to a Telegram bot when a predefined patter is detected.
- **Chart Generation**: Utilizes `plotly` to generate and upload charts to Telegram admins for visual analysis.
- **Data Handling**: Employs `ccxt` for exchange data and `pandas` for data manipulation.
