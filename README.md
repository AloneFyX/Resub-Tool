# Resub-Tool
Resub Tool By Alone.io7


# Nitro Resubscribe Bot

A simple Python script to automatically re-subscribe Discord Nitro using fresh VCCs (virtual credit cards) and notify you via Discord webhook.

## 🚀 Features

- Load multiple Discord account tokens and VCCs from text files
- Add a new VCC to each account via Discord API
- Purchase 1-month Nitro subscription automatically
- Log results (`Success` or error) to `results.txt`
- Send rich embed notifications to your Discord channel via webhook

## 🛠️ Requirements

- Python 3.8+
- `requests` library

```bash
pip install requests
```

## 📁 File Structure

```
├── README.md
├── main.py               # Main script (nitro_resubscribe_bot)
├── tokens.txt           # One Discord token per line
├── vcc.txt              # One VCC per line: card|exp_month|exp_year|cvc
├── results.txt          # Logs of each attempt
```

## ⚙️ Configuration

1. **Edit `main.py`**:
   - At the top of the file, set your Discord webhook URL:
     ```python
     WEBHOOK_URL = "https://your.webhook.url/here"
     ```

2. **Prepare `tokens.txt`**:
   - Add one Discord token per line (e.g., `mfa.xxxxx...`).

3. **Prepare `vcc.txt`**:
   - Add one VCC per line in the format:
     ```text
     4111111111111111|12|2026|123
     ```

## 💻 Usage

Run the script from your terminal:

```bash
python main.py
```

- The script will iterate through each token:
  1. Add the corresponding VCC as a payment source
  2. Attempt to purchase Nitro Monthly
  3. Log the result in `results.txt`
  4. Send a Discord webhook notification

## 📊 Logging

- `results.txt` will contain entries like:
  ```text
  mfa.xxxxxxxxxxxxxxxxxxxxx... => Success
  mfa.yyyyyyyyyyyyyyyyyyyyy... => Failed to add VCC
  ```

## 🔔 Notifications

- After each attempt, you will receive an embed in your configured Discord channel:
  - **Token** (first 25 characters)
  - **Status** (Success / Failure)
  - **Card Used** (last 4 digits)

## ⚖️ License

This project is provided as-is under the MIT License. See [LICENSE](LICENSE) for details.

---

*Use responsibly. Abuse may violate Discord's Terms of Service.*

