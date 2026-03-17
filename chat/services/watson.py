import requests
from django.conf import settings


class WatsonAPIError(Exception):
    pass


def get_ibm_iam_token() -> str:
    api_key = settings.IBM_WATSON_API_KEY
    if not api_key:
        raise WatsonAPIError("Missing IBM_WATSON_API_KEY")

    response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "apikey": api_key,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise WatsonAPIError(
            f"Failed to get IAM token: {response.status_code} {response.text}"
        )

    data = response.json()
    token = data.get("access_token")
    if not token:
        raise WatsonAPIError("IAM response missing access_token")

    return token


def build_payload(user_text: str, student_context: dict | None = None) -> dict:
    context = student_context or {}

    context_text = ""
    if context:
        profile = context.get("student_profile", {})
        context_text = (
            "Student profile:\n"
            f"- Campus: {profile.get('campus', '')}\n"
            f"- Major: {profile.get('major', '')}\n"
            f"- Year: {profile.get('year', '')}\n"
            f"- Current classes: {profile.get('current_classes', '')}\n"
            f"- Career goals: {profile.get('career_goals', '')}\n"
            f"- Interests: {profile.get('interests', '')}\n"
            f"- Target roles: {profile.get('target_roles', '')}\n"
            f"- Skills: {profile.get('skills', '')}\n"
            f"- Available hours/week: {profile.get('available_hours_per_week', '')}\n\n"
        )

    final_prompt = (
        "You are CareerCompass AI, a concise and supportive career mentor for CSU students.\n"
        "Give one next best action first, then 2-4 relevant supporting suggestions.\n"
        "Only recommend things relevant to the student's profile and message.\n\n"
        f"{context_text}"
        f"Student message: {user_text}"
    )

    return {
        "messages": [
            {
                "role": "user",
                "content": final_prompt,
            }
        ]
    }


def extract_reply(data: dict) -> str:
    if isinstance(data, dict):
        if "choices" in data and data["choices"]:
            choice = data["choices"][0]
            message = choice.get("message", {})
            content = message.get("content")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                text_parts = []
                for item in content:
                    if isinstance(item, dict) and isinstance(item.get("text"), str):
                        text_parts.append(item["text"])
                if text_parts:
                    return "\n".join(text_parts)

        if "results" in data and data["results"]:
            first = data["results"][0]
            if isinstance(first, dict):
                generated = first.get("generated_text")
                if isinstance(generated, str) and generated.strip():
                    return generated

        if "output" in data and isinstance(data["output"], str):
            return data["output"]

    return "I received a response, but could not extract the mentor reply."


def chat_with_watson(user_text: str, student_context: dict | None = None) -> str:
    token = get_ibm_iam_token()

    response = requests.post(
        f"{settings.IBM_WATSON_DEPLOYMENT_URL}?version={settings.IBM_WATSON_VERSION}",
        json=build_payload(user_text, student_context),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        timeout=60,
    )

    if response.status_code != 200:
        raise WatsonAPIError(
            f"Watson deployment call failed: {response.status_code} {response.text}"
        )

    try:
        data = response.json()
    except ValueError:
        raise WatsonAPIError("Watson returned non-JSON output")

    return str(data)