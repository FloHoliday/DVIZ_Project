# Menthal Health Dashboard

This project is a interactive dashboard built with Dash that visualizes the correlation between mental Health disorders and societal factors.

## Requirements

- Python 3.13.0
- pip (Python package installer, usually comes with Python)

## Installation

1. Extract the archive and navigate to the created directory

```bash
cd Mental_Health_Dashboard
```

2. Create a virtual environment (recomended), we suggest python 3.13.0

```bash
# Windows
python -m venv dashboard_mental_health
.\dashboard_mental_health\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

## Running the Application

1. Ensure your virtual environment is activated
2. Install dependencies

```bash
make install
```

3. Run the application:

```bash
make run
```

Note: The first start-up can take up to two minutes

4. Open your web browser and navigate to `http://127.0.0.1:8050/`

### Project Structure

```bash
Mental_Health_Dashboard/
├── Dashboard/
│   ├── __pycache__/
│   ├──assets/
│   │    ├── img/
│   │    └── styles.css
│   ├── data/
│   │    ├── mental_health_and_indicators.csv
│   ├── corr_explain_functions.py              # Correlation explanation helpers
│   ├── corr_graph_functions.py                # Correlation graph generators
│   ├── country_comparison_functions.py        # Country comparison logic
│   ├── donut_graph_functions.py               # Donut chart generators
│   ├── friendly_names.py                      # Display name mappings
│   ├── main.py                                # Core data processing
│   ├── map_functions.py                       # Map visualization functions
│   └── requirements.txt                       # Dependencies
├── .gitignore
├── Makefile                                   # Build automation
└── README.md                                  # Documentation
```

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

We originally found the dataset on the mental health disroders on ourworldindata.org:

- Saloni Dattani, Lucas Rodés-Guirao, Hannah Ritchie and Max Roser (2023) - “Mental Health” Published online at OurWorldinData.org: https://ourworldindata.org/mental-health

While the dataset is discussed and visualized on OurWorldinData.org, it was downloaded from [Kaggle](https://www.kaggle.com/datasets/imtkaggleteam/mental-health) for use in this project.

We used the following datasets from data.worldbank.org for the indicators:

- GDP, in $: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
- Health Expenditure, in $, PPP: https://data.worldbank.org/indicator/SH.XPD.CHEX.PP.CD
- CO2 Emissions, in Mt CO2e: https://data.worldbank.org/indicator/EN.GHG.CO2.MT.CE.AR5
- Unemployment rate, in %: https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS
- Life expectancy, in years: https://data.worldbank.org/indicator/SP.DYN.LE00.IN

## Contact

If you have any questions, please contact us here:

- Finn Eyer: finn.eyer@stud.hslu.ch
- Florian Item: florian.item@stud.hslu.ch
- Karim Darwiche: karim.darwiche@stud.hslu.ch
