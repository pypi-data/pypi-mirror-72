import re

from coconut import Response
from coconut.utils import classproperty


class LmtIndiaCovid19Response(Response):
    @property
    def phone_number(self):
        return str(self.data["phoneINT[SQ001]"])

    @property
    def timestamp(self):
        return str(self.data["submitdate"])

    @property
    def num_risk_factors(self):
        return sum(
            (
                self.potential_threat_of_domestic_violence,
                self.potential_debt_bondage_or_forced_labor,
                self.medical_emergency,
                self.food_security_risk,
                self.potentially_stranded,
            )
        )

    @property
    def max_risk_priority(self):
        max_risk = 3
        for condition, priority in (
            (self.potential_threat_of_domestic_violence, 1),
            (self.potential_debt_bondage_or_forced_labor, 1),
            (self.medical_emergency, 1),
            (self.food_security_risk, 1),
            (self.potentially_stranded, 2),
        ):
            if condition:
                max_risk = min(max_risk, priority)
        return max_risk

    @property
    def sort_order(self):
        return (-1 * self.num_risk_factors, self.max_risk_priority, self.id)

    @classproperty
    def risk_columns(self):
        return [
            "id",
            "phoneINT[SQ001]",
            "submitdate",
            "currentCity",
            "risk[priority]",
            "risk[numFactors]",
            "risk[domesticViolence]",
            "risk[forcedLabor]",
            "risk[medicalEmergency]",
            "risk[foodSecurity]",
            "risk[stranded]",
            "domesticViolence[subjToViolence]",
            "domesticViolence[recvThreatsFamily]",
            "forcedLabor[recvThreatsLawEnf]",
            "forcedLabor[recvThreatsEmp]",
            "forcedLabor[lvEmployerOwesMoney]",
            "forcedLabor[lvEmployerThreatensMe]",
            "forcedLabor[lvEmployerPayDebt]",
            "medicalEmergency[needsImmediate]",
            "medicalEmergency[pregnantFamilyImmediate]",
            "foodSecurity[noSavings]",
            "foodSecurity[noIncome]",
            "foodSecurity[needsDryRations]",
            "foodSecurity[needsCookedFood]",
            "foodSecurity[notEatenProperly]",
            "stranded[needsTransportHome]",
            "stranded[inTransitCantComplete]",
        ]

    @property
    def risk_data(self):
        return {
            "id": self.id,
            "phoneINT[SQ001]": self.phone_number,
            "submitdate": self.timestamp,
            "currentCity": self.current_city,
            "risk[priority]": self.max_risk_priority,
            "risk[numFactors]": self.num_risk_factors,
            "risk[domesticViolence]": self.potential_threat_of_domestic_violence,
            "risk[forcedLabor]": self.potential_debt_bondage_or_forced_labor,
            "risk[medicalEmergency]": self.medical_emergency,
            "risk[foodSecurity]": self.food_security_risk,
            "risk[stranded]": self.potentially_stranded,
            "domesticViolence[subjToViolence]": self.subjected_to_violence,
            "domesticViolence[recvThreatsFamily]": self.receiving_threats_family_friends,
            "forcedLabor[recvThreatsLawEnf]": self.receiving_threats_law_enforcement,
            "forcedLabor[recvThreatsEmp]": self.receiving_threats_recruiter,
            "forcedLabor[lvEmployerOwesMoney]": self.cannot_leave_employer_because_employer_owes_money,
            "forcedLabor[lvEmployerThreatensMe]": self.cannot_leave_employer_because_he_threatens_me,
            "forcedLabor[lvEmployerPayDebt]": self.cannot_leave_employer_because_i_need_to_pay_debt,
            "medicalEmergency[needsImmediate]": self.needs_immediate_medical_support,
            "medicalEmergency[pregnantFamilyImmediate]": self.has_pregnant_family_member_or_needs_immediate_assistance,
            "foodSecurity[noSavings]": self.has_no_savings,
            "foodSecurity[noIncome]": self.has_no_household_income,
            "foodSecurity[needsDryRations]": self.has_immediate_need_for_dry_rations,
            "foodSecurity[needsCookedFood]": self.has_immediate_need_for_cooked_food,
            "foodSecurity[notEatenProperly]": self.has_not_eaten_properly_in_a_few_days,
            "stranded[needsTransportHome]": self.needs_transport_back_home,
            "stranded[inTransitCantComplete]": self.in_transit_and_has_no_means_to_complete_journey,
        }

    @property
    def potential_threat_of_domestic_violence(self):
        return any((self.subjected_to_violence, self.receiving_threats_family_friends))

    @property
    def receiving_threats_family_friends(self):
        return self.bool("violenceWho[SQ005]")

    @property
    def subjected_to_violence(self):
        return self.bool("immediateAssistance[SQ006]")

    @property
    def potential_debt_bondage_or_forced_labor(self):
        return any(
            (
                self.receiving_threats_law_enforcement,
                self.receiving_threats_recruiter,
                self.cannot_leave_employer_because_employer_owes_money,
                self.cannot_leave_employer_because_he_threatens_me,
                self.cannot_leave_employer_because_i_need_to_pay_debt,
            )
        )

    @property
    def receiving_threats_law_enforcement(self):
        return self.bool("violenceWho[SQ003]")

    @property
    def receiving_threats_recruiter(self):
        return self.bool("violenceWho[SQ003]")

    @property
    def cannot_leave_employer_because_employer_owes_money(self):
        return self.str_match("leaveEmployer", "No because he owes me money")

    @property
    def cannot_leave_employer_because_he_threatens_me(self):
        return self.str_match(
            "leaveEmployer", "No because he threatens me and or my family"
        )

    @property
    def cannot_leave_employer_because_i_need_to_pay_debt(self):
        return self.str_match(
            "leaveEmployer", "No because I need to pay off my debt or advance"
        )

    @property
    def medical_emergency(self):
        return any(
            (
                self.needs_immediate_medical_support,
                self.has_pregnant_family_member_or_needs_immediate_assistance,
            )
        )

    @property
    def needs_immediate_medical_support(self):
        return self.bool("supportRequest[SQ006]")

    @property
    def has_pregnant_family_member_or_needs_immediate_assistance(self):
        return self.bool("immediateAssistance[SQ002]")

    @property
    def food_security_risk(self):
        return (
            self.has_no_savings
            and self.has_no_household_income
            and any(
                (
                    self.has_immediate_need_for_dry_rations,
                    self.has_immediate_need_for_cooked_food,
                    self.has_not_eaten_properly_in_a_few_days,
                )
            )
        )

    @property
    def has_no_savings(self):
        return self.str_match("supportSelfDependent", "I have no savings")

    @property
    def has_no_household_income(self):
        try:
            return int(self.data["currentHouseholdInco"]) == 0
        except TypeError:
            return False

    @property
    def has_immediate_need_for_dry_rations(self):
        return self.bool("supportRequest[SQ003]")

    @property
    def has_immediate_need_for_cooked_food(self):
        return self.bool("supportRequest[SQ004]")

    @property
    def has_not_eaten_properly_in_a_few_days(self):
        return self.bool("immediateAssistance[SQ004]")

    @property
    def potentially_stranded(self):
        return any(
            (
                self.needs_transport_back_home,
                self.in_transit_and_has_no_means_to_complete_journey,
            )
        )

    @property
    def needs_transport_back_home(self):
        return self.bool("supportRequest[SQ005]")

    @property
    def in_transit_and_has_no_means_to_complete_journey(self):
        return self.bool("immediateAssistance[SQ003]")

    @property
    def current_city(self):
        city = self.data["currentCity"]
        if city == "Other":
            return self.data["currentCity[other]"]
        return city

    def bool(self, key):
        return getbool(self.data[key])

    def str_match(self, key, value):
        val = str(self.data[key]).lower().strip()
        val = re.sub(r"[^A-Za-z0-9 ]", " ", val)
        val = re.sub(r" +", " ", val)
        return val == value.lower().strip()


def getbool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        return value.lower() in ("yes", "y", "true", "1")
    return False
