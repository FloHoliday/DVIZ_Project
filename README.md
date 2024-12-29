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

2. Create a virtual environment (optional)
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


## Attributions
We pulled the dataset regarding to the mental health disroders from ourworldindata.org:
- Saloni Dattani, Lucas Rodés-Guirao, Hannah Ritchie and Max Roser (2023) - “Mental Health” Published online at OurWorldinData.org. Retrieved from: 'https://ourworldindata.org/mental-health' [Online Resource]

We used the following Datasets from data.worldbank.org under the Creative Commons Attribution 4.0 (CC-BY 4.0).
Indicators:
- GDP, in $: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
- Health Expenditure, in $, PPP: https://data.worldbank.org/indicator/SH.XPD.CHEX.PP.CD
- CO2 Emissions: https://data.worldbank.org/indicator/EN.GHG.CO2.MT.CE.AR5?view=map
- Unemployment rate: https://data.worldbank.org/indicator/EN.GHG.CO2.MT.CE.AR5
- Life expectancy: https://data.worldbank.org/indicator/SP.DYN.LE00.IN

## Contact
If you have any questions, please contact us here:
- Finn Eyer: finn.eyer@stud.hslu.ch
- Florian Item: florian.item@stud.hslu.ch
- Karim Darwiche: karim.darwiche@stud.hslu.ch
