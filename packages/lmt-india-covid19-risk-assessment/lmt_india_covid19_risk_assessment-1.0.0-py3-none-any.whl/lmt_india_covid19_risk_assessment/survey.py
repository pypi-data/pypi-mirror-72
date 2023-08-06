from coconut.survey import Survey
from coconut.utils import classproperty

from lmt_india_covid19_risk_assessment.response import LmtIndiaCovid19Response
import pandas as pd


class LmtIndiaCovid19RiskAssessment(Survey):
    @property
    def title(self):
        """Overrides the default survey title"""
        return "LMT-India COVID-19 Risk Assessment"

    @property
    def dataframe(self):
        """Defines the dataframe to be exported when exporting CSV files"""
        return self._risk_dataframe()

    @classproperty
    def response_cls(cls):
        """Uses this response class when loading responses from LimeSurvey"""
        return LmtIndiaCovid19Response

    def _risk_dataframe(self):
        """Creates a dataframe containing information about each survey question"""
        rows = list(self.responses_by_id.values())
        rows = sorted(rows, key=lambda x: x.sort_order)
        rows = [r.data for r in rows if r.num_risk_factors > 0]
        return pd.DataFrame(rows, columns=LmtIndiaCovid19Response.risk_columns)

    def _response_dataframe(self):
        """Creates a dataframe containing information about each survey question"""
        rows = list(self.responses_by_id.values())
        rows = sorted(rows, key=lambda x: x.sort_order)
        rows = [r.data for r in rows if r.num_risk_factors > 0]
        return pd.DataFrame(rows)

    @property
    def worksheets(self):
        """Defines the worksheets to be included in an Excel or Google Sheets workbook"""
        return [
            ("Risk Assessment", self._risk_dataframe()),
            ("Responses", self._response_dataframe()),
            ("Questions", self._question_dataframe()),
            ("Question Groups", self._question_group_dataframe())
        ]
