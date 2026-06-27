
class RecommendationEngine:
    def build(self, patient, results):

        report = {

            "health_score":

                self.health_score(results),

            "overall_risk":

                self.risk_level(

                    max(

                        results["diabetes_probability"],

                        results["hypertension_probability"],

                        results["hyperlipidemia_probability"]

                    )

                ),

            "reasons":

                self.explain_risk(patient),

            "recommendations":

                self.lifestyle_recommendations(patient),

            "tests":

                self.suggested_tests(results)

        }

        return report
    def suggested_tests(self, results):

        tests = []

        if results["diabetes_probability"] >= 0.40:

            tests.extend([

                "HbA1c",

                "Fasting Blood Glucose"

            ])

        if results["hypertension_probability"] >= 0.40:

            tests.append(

                "Blood Pressure Measurement"

            )

        if results["hyperlipidemia_probability"] >= 0.40:

            tests.append(

                "Lipid Profile"

            )

        if len(tests) == 0:

            tests.append(

                "Annual routine medical check-up"

            )

        return tests
    def lifestyle_recommendations(self, patient):

        recommendations = []

        if patient["bmi"] >= 25:

            recommendations.append(
                "Maintain a healthy body weight."
            )

        if patient["exercise_days_per_week"] < 3:

            recommendations.append(
                "Exercise at least 150 minutes per week."
            )

        if patient["soft_drinks_per_week"] >= 5:

            recommendations.append(
                "Reduce sugary drinks."
            )

        if patient["fast_food_meals_per_week"] >= 3:

            recommendations.append(
                "Reduce fast-food consumption."
            )

        if patient["sleep_hours"] < 7:

            recommendations.append(
                "Sleep 7-9 hours every night."
            )

        if patient["smoking_status"] == "Current":

            recommendations.append(
                "Quit smoking."
            )

        if patient["daily_sitting_hours"] >= 8:

            recommendations.append(
                "Reduce sitting time and move regularly."
            )

        if len(recommendations) == 0:

            recommendations.append(
                "Keep your current healthy lifestyle."
            )

        return recommendations
        

    def family_scores(self, patient):

        diabetes = (

            patient["father_diabetes"] * 4 +

            patient["mother_diabetes"] * 4 +

            patient["paternal_grandparents_diabetes"] +

            patient["maternal_grandparents_diabetes"]

        )

        hypertension = (

            patient["father_hypertension"] * 4 +

            patient["mother_hypertension"] * 4 +

            patient["paternal_grandparents_hypertension"] +

            patient["maternal_grandparents_hypertension"]

        )

        hyperlipidemia = (

            patient["father_hyperlipidemia"] * 4 +

            patient["mother_hyperlipidemia"] * 4 +

            patient["paternal_grandparents_hyperlipidemia"] +

            patient["maternal_grandparents_hyperlipidemia"]

        )

        return diabetes, hypertension, hyperlipidemia



    def risk_level(self, probability):

        if probability < 0.30:
            return "Low"

        elif probability < 0.60:
            return "Moderate"

        return "High"


    def health_score(self, results):

        avg = (

            results["diabetes_probability"]

            +

            results["hypertension_probability"]

            +

            results["hyperlipidemia_probability"]

        ) / 3

        return round((1 - avg) * 100)
    


    def explain_risk(self, patient):

        diabetes_family_score, hypertension_family_score, hyperlipidemia_family_score = self.family_scores(patient)

        reasons = []
        

        if patient["bmi"] >= 30:

            reasons.append(
                "High Body Mass Index (BMI)"
            )

        if patient["smoking_status"] == "Current":

            reasons.append(
                "Current smoker"
            )

        if patient["exercise_days_per_week"] < 3:

            reasons.append(
                "Low physical activity"
            )

        if patient["soft_drinks_per_week"] >= 5:

            reasons.append(
                "Frequent sugary drinks"
            )

        if patient["fast_food_meals_per_week"] >= 3:

            reasons.append(
                "Frequent fast food"
            )

        if patient["sleep_hours"] < 6:

            reasons.append(
                "Poor sleep duration"
            )

        if diabetes_family_score >= 4:

            reasons.append(
                "Positive family history of diabetes"
            )

        if hypertension_family_score >= 4:

            reasons.append(
                "Positive family history of hypertension"
            )

        if hyperlipidemia_family_score >= 4:

            reasons.append(
                "Positive family history of hyperlipidemia"
            )

        return reasons
    
    
engine = RecommendationEngine()
    
