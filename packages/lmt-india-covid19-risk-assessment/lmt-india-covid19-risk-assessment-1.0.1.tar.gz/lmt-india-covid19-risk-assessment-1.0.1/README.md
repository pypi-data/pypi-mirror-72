# lmt-india-covid19-risk-assessment

Defines survey type `LmtIndiaCovid19RiskAssessment` and response `LmtIndiaCovid19Response` using [coconut](https://github.com/istresearch/coconut)


## Installation

```
pip install lmt-india-covid19-risk-assessment
```

## Usage

```python
from coconut import LimeAPI, Workbook
from lmt_india_covid19_risk_assessment import LmtIndiaCovid19RiskAssessment

# Create a LimeAPI instance
lime = LimeAPI(
        url="https://surveys.my-lime-survey-instance.org",
        username="admin",
        password="password"
    )

# Create the survey instance
survey = LmtIndiaCovid19RiskAssessment(survey_id=119618, lime_api=lime)

# Load questions, responses, survey info
survey.load_data()

# Save the data to an Excel file
survey.to_excel("survey.xlsx")

# Save response data to a CSV file
survey.to_csv("survey.csv")

# Update a Google Sheets workbook
workbook = Workbook(
    workbook_id="abc123",
    survey=survey,
    service_account_json_path="google-cloud-creds.json"
)
workbook.sync()
```