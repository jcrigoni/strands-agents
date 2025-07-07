# strands-concierge-streamlit

This project implements a concierge agent that assists users in finding restaurants based on weather conditions and making reservations. The agent utilizes various tools for weather assistance, restaurant finding, datetime parsing, and table reservation.

## Project Structure

```
strands-concierge-streamlit
├── src
│   ├── agent.py         # Implementation of the concierge agent and its tools
│   └── app.py           # Streamlit application for user interaction
├── requirements.txt      # List of project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd strands-concierge-streamlit
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment. You can create one using `venv` or `conda`.

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application**:
   Navigate to the `src` directory and run the following command:
   ```bash
   streamlit run app.py
   ```

## Usage Guidelines

- Once the application is running, you will see a chat interface where you can ask questions related to restaurant recommendations based on weather conditions.
- The concierge agent will respond with suggestions for outdoor or indoor dining options based on the current weather and your preferences.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.