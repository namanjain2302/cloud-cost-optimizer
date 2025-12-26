from src.llm_client import query_llm

REQUIRED_PROFILE_KEYS = {
    "name",
    "budget_inr_per_month",
    "description",
    "tech_stack",
    "non_functional_requirements"
}

def extract_project_profile(description_text):
    system_prompt = (
        "You are a Cloud Architect. Extract project details into a STRICT JSON object. "
        "Return ONLY valid JSON. No markdown. No explanations."
    )

    user_prompt = f"""
    Analyze the following project description and extract these fields:
    - name (string)
    - budget_inr_per_month (number)
    - description (cleaned string)
    - tech_stack (object)
    - non_functional_requirements (array of strings)

    Input Text:
    "{description_text}"
    """

    profile = query_llm(system_prompt, user_prompt)

    # 🔒 HARD VALIDATION
    if not isinstance(profile, dict):
        raise ValueError("Project profile must be a JSON object")

    if not REQUIRED_PROFILE_KEYS.issubset(profile.keys()):
        raise ValueError("Incomplete project profile returned by LLM")

    return profile
def generate_mock_billing(profile_json: dict) -> list:
    budget = profile_json["budget_inr_per_month"]
    tech_stack = profile_json["tech_stack"]

    system_prompt = (
        "You are a Cloud Billing Generator.\n"
        "Return ONLY a valid JSON ARRAY.\n"
        "Do NOT truncate output."
    )

    user_prompt = f"""
Generate EXACTLY 6 billing records.

Tech Stack: {tech_stack}
Monthly Budget: {budget}

Each record MUST follow this schema:
{{
  "month": "YYYY-MM",
  "service": "string",
  "resource_id": "string",
  "region": "string",
  "usage_quantity": number,
  "unit": "string",
  "cost_inr": number,
  "desc": "string"
}}

Return ONLY the JSON array.
"""

    billing = query_llm(
        system_prompt,
        user_prompt,
        expected_type="array"
    )

    for item in billing:
        if not isinstance(item, dict) or "cost_inr" not in item:
            raise ValueError("Invalid billing item")

    return billing

def generate_optimization_report(profile_json, billing_data):
    if not isinstance(profile_json, dict):
        raise ValueError("Profile must be a dict")

    if not isinstance(billing_data, list):
        raise ValueError("Billing data must be a list")

    # ✅ SAFE aggregation
    total_cost = sum(item["cost_inr"] for item in billing_data)
    budget = profile_json.get("budget_inr_per_month", 0)

    service_costs = {}
    for item in billing_data:
        svc = item["service"]
        service_costs[svc] = service_costs.get(svc, 0) + item["cost_inr"]

    analysis_summary = {
        "total_monthly_cost": total_cost,
        "budget": budget,
        "budget_variance": total_cost - budget,
        "is_over_budget": total_cost > budget,
        "service_costs": service_costs
    }

    system_prompt = (
        "You are a Senior FinOps Consultant. "
        "Return STRICT JSON only."
    )

    user_prompt = f"""
    Project Profile:
    {profile_json}

    Spending Analysis:
    {analysis_summary}

    Billing Sample:
    {billing_data[:5]}

    Generate a Cost Optimization Report with 4–6 recommendations.
    """

    report = query_llm(system_prompt, user_prompt)

    # 🔒 FINAL VALIDATION
    if not isinstance(report, dict):
        raise ValueError("Optimization report must be a JSON object")

    return report
