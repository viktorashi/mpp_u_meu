from flask import Flask

app = Flask(__name__)

# Example configuration
app.config['DEBUG'] = True
# Add other configurations as needed

# Import your routes to register them with the application
from app import routes