# Kashu

Kashu is a project designed to run python kwic programs on the web.

## How to Run on the Web

1. Clone this repository:
   ```bash
   git clone https://github.com/amesyu/kashu.git
   cd kashu
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the web server (update this step based on your actual entry point, e.g., Flask, Django, Streamlit, etc.):
   ```bash
   # Example using Flask:
   export FLASK_APP=app.py
   flask run
   ```

4. Open your browser and navigate to `http://localhost:5000` (or the port your app uses).

## Project Structure

- Python files for backend logic
- Web interface to interact with Python code

## Requirements

See [requirements.txt](requirements.txt) for required Python packages.
