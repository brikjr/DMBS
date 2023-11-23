# Financial Advisor Web App

This is a basic web application for financial management using Flask and MySQL.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python

#### Virutal env for python
```python -m venv dbms```

###### Activate the virtual environment
```source dbms/bin/activate```  # On macOS/Linux

###### or
```source\Scripts\activate```  # On Windows

###### Install dependencies
```pip install -r requirements.txt```  # or install each package individually


## Setup

1. Clone the repository:

   ```git clone https://github.com/yourusername/financial-advisor-app.git```

2. Run the application:
```python app.py```

Open your web browser and go to http://127.0.0.1:5000

3. Usage
Access the application by visiting http://127.0.0.1:5000 in your web browser.
Use the provided login functionality to access the home page.
Navigate through the application to manage your financial data.

4. Customization
Make sure to replace URL in config.json with the correct connection details for your MySQL server. This URI should follow the format 'mysql://username:password@host/database'. Adjust it based on your MySQL username, password, host, and database name.