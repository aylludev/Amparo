import requests

def get_departments():
    url = "https://raw.githubusercontent.com/marcovega/colombia-json/master/colombia.min.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        departments = [dept["departamento"] for dept in data]
        return sorted(departments)
    
    return ["Error fetching API"]
