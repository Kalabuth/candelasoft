import requests

def fetch_external_data(email):
    try:
        url = f"https://gorest.co.in/public/v2/users?email={email}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("data", data)
        if not data:
            return {
                "status": "inactive",
                "plan": "basic",
                "company": "Desconocida"
            }

        user_data = data[0]
        status = user_data.get("status", "inactive")

        return {
            "status": status,
            "plan": "premium" if status == "active" else "basic",
            "company": user_data.get("name", "Desconocida")
        }

    except requests.RequestException:
        return {
            "status": "inactive",
            "plan": "basic",
            "company": "Desconocida"
        }
