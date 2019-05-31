import json
import requests
from datetime import date

with open('./config.json', 'r') as f:
    config = json.load(f)

headers = {"Authorization": "Bearer " + config["secret"]}
base_url = "https://api.youneedabudget.com/v1/budgets/" +config["budget"] + '/'

current_balance = float(requests.get(
    base_url + "accounts/" + config["account"],
    headers=headers).json()["data"]["account"]["balance"])

conversion_rate = float(requests.get("https://blockchain.info/ticker").json()["USD"]["15m"])

new_balance = conversion_rate * float(config["holdings"]) * 1000

data = {
    "transaction": {
      "account_id": config["account"],
        "date": date.today().isoformat(),
        "amount": int(new_balance-current_balance),
        "payee_name": "Coal Correction",
        "category_id": config["category"],
        "memo": "",
        "cleared": "reconciled",
        "approved": True,
        "flag_color": "blue"
    }
}

response = requests.post(base_url + "transactions", json=data, headers=headers)
print(response.json())
