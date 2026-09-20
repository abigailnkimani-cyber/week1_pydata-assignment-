# Employment-to-population ratios by gender

A CRISP-DM analysis of employment-to-population ratio across countries, with a focus on the gender gap, and an interactive Streamlit dashboard.

Live app: (http://localhost:8506/)

## Research question

What is the size of the gender gap in employment-to-population ratios across countries?

Which countries have the largest and smallest ratios and gaps?

## Dataset
• Source: https://ilostat.ilo.org/data/snapshots/employment-to-population-ratio/
• Contains employment-to-population ratio (%), for the total population, men, and women, by area and reference year
• 312 records: 225 countries and territories plus 87 aggregates (regions, income groups, and country groupings)
• One record per area with a single reference year; it is therefore a cross-section and therefore cannot be used to compare trends
## Method (CRISP-DM)
1. Business understanding: formulate the gender-gap question
2. Data understanding: inspect structure, coverage, missing values, and outliers
3. Data preparation:
- remove the 87 aggregates, which are modelled projections dated 2027
- keep country records for 1991-2025
- remove 6 countries with a missing male or female value (225 → 219)
- create `Gap` = male ratio − female ratio, in percentage points, rounded to 2 decimals
4. Modeling: descriptive statistics, rankings, and a male-against-female comparison
5. Evaluation: test findings against the research question; state limitations
6. Deployment: publish results as a Streamlit app, showing the 15 highest employment ratios, a male-against-female scatter plot, and the 15 largest gender gaps
## Key findings
• The median employment ratio is 58.7% and the median gender gap is 12.94 percentage points
• A gap below 10 points exists in 79 of 219 countries (36%) and a gap of over 30 points in 34 (16%); 15 countries have a gap of over 40 points
• The largest gaps are in the Syrian Arab Republic (57.6), Yemen (52.9), and Pakistan (51.2)
• Male and female ratios are moderately correlated (r = 0.61)
• Kenya's gap is 11.61 points (2021), just below the median
## Repository structure
```
├── week1_ass_pydata.ipynb          Analysis and cleaning
├──                              Streamlit dashboard
├── requirements.txt             Python dependencies
├── data/
│  └── cleaned_employment_ratio.csv    Cleaned country data used by the app
└── README.md
```
## Run locally
```python
streamlit_process = subprocess.Popen(["streamlit", "run", "app.py"])
```
```bash
pip install -r requirements.txt
```
The app opens at (http://localhost:8506/)
## Limitations
• Reference years range from 1991 to 2025; 32 records are before 2015, meaning that the figures are not measured in the same year
• Countries with missing sex-disaggregated values were excluded, meaning that the rankings do not represent those countries
• The employment-to-population ratio combines labour force participation and unemployment; it does not capture unpaid care work and all informal work
• The results capture association only and do not explain the causes of the differences

## Author

Abby