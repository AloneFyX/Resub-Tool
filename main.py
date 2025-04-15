import requests
import time

# ==== CONFIGURATION ====
WEBHOOK_URL = "https://your.webhook.url/here"  # <- Set your Discord webhook URL here

# Load tokens and VCCs
def load_tokens():
    with open("tokens.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def load_vccs():
    with open("vcc.txt", "r") as f:
        return [line.strip().split("|") for line in f if line.strip()]

def log_result(token, status):
    with open("results.txt", "a") as f:
        f.write(f"{token[:25]}... => {status}\n")

def send_webhook(token, status, card_number):
    if not WEBHOOK_URL:
        return

    payload = {
        "embeds": [
            {
                "title": "\u2705 Token Resubscribe Attempt",
                "color": 0x00ff00 if "Success" in status else 0xff0000,
                "fields": [
                    {"name": "Token", "value": f"`{token[:25]}...`", "inline": False},
                    {"name": "Status", "value": status, "inline": True},
                    {"name": "Card Used", "value": f"`•••• {card_number[-4:]}`", "inline": True}
                ],
                "footer": {"text": "Nitro ReSub Bot"}
            }
        ]
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except:
        pass

def add_vcc(token, card_number, exp_month, exp_year, cvc):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Discord/23785"
    }

    payload = {
        "type": 1,
        "billing_address": {
            "name": "John Doe",
            "line_1": "123 Fake Street",
            "city": "Testville",
            "state": "CA",
            "country": "US",
            "postal_code": "12345"
        },
        "payment_gateway": "stripe",
        "payment_source": {
            "number": card_number,
            "exp_month": int(exp_month),
            "exp_year": int(exp_year),
            "cvc": cvc
        }
    }

    r = requests.post("https://discord.com/api/v9/users/@me/billing/payment-sources", headers=headers, json=payload)
    if r.status_code == 200:
        return r.json().get("id")  # Payment source ID
    return None

def purchase_nitro(token, payment_source_id):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Discord/23785"
    }

    payload = {
        "sku_id": "521847234246082599",  # Nitro Monthly
        "payment_source_id": payment_source_id,
        "gateway_checkout_context": {
            "payment_source_id": payment_source_id
        }
    }

    r = requests.post("https://discord.com/api/v9/store/skus/521847234246082599/purchase", headers=headers, json=payload)
    return r.status_code == 200

def main():
    tokens = load_tokens()
    vccs = load_vccs()

    for i, token in enumerate(tokens):
        if i >= len(vccs):
            print("Not enough VCCs for all tokens!")
            break

        card_number, exp_month, exp_year, cvc = vccs[i]
        print(f"[+] Processing token {i+1}/{len(tokens)}")

        try:
            payment_source_id = add_vcc(token, card_number, exp_month, exp_year, cvc)
            if payment_source_id:
                success = purchase_nitro(token, payment_source_id)
                status = "Success" if success else "Failed at purchase"
            else:
                status = "Failed to add VCC"

        except Exception as e:
            status = f"Error: {e}"

        log_result(token, status)
        send_webhook(token, status, card_number)
        time.sleep(2)  # Prevent rate limit

if __name__ == "__main__":
    main()
