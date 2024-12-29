# Data Story Dashboard

This project is a interactive dashboard built with Dash that visualizes the correlation between mental Health disorders and societal factors.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer, usually comes with Python)

## Installation

1. Clone this repository
```bash
git clone https://github.com/FloHoliday/DVIZ_Project/
cd DVIZ_Project
```

2. Create a virtual environment
```bash
# Windows
python -m venv dashboard_mental_health
.\dashboard_mental_health\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

1. Ensure your virtual environment is activated
2. Run the application:
```bash
python main.py
```
3. Open your web browser and navigate to `http://127.0.0.1:8050/`

## Development

### Dependencies
The project uses the following main libraries:
- Dash - Web application framework
- Pandas - Data manipulation and analysis
- Plotly - Interactive visualizations
- NumPy - Numerical computing
- SciPy - Scientific computing

For a complete list of dependencies, see `requirements.txt`.

## Usage

[Describe how to use your application, including:]
- Main features
- How to interact with the visualizations
- Any specific functionality users should know about

## Troubleshooting

Common issues and solutions:

1. Port 8050 is already in use
   - Solution: Change the port in app.py:
     ```python
     app.run_server(debug=True, port=[different-port-number])
     ```

2. Missing dependencies
   - Solution: Ensure all requirements are installed:
     ```bash
     pip install -r requirements.txt
     ```

3. Virtual environment issues
   - Solution: Delete the mental_health_dashboard folder and recreate:
     ```bash
     # Windows
     rmdir venv /s /q
     # macOS/Linux
     rm -rf venv
     
     # Then recreate
     python -m venv venv
     ```

## Contact
If you have any questions, please contact us here:
- Finn Eyer: finn.eyer@stud.hslu.ch
- Florian Item: florian.item@stud.hslu.ch
- Karim Darwiche: karim.darwiche@stud.hslu.ch
