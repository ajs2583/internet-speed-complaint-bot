# Internet Speed Complaint Bot 

This Python bot checks your internet speed using Speedtest.net and tweets at your internet provider (or university) if your speeds are lower than expected. Built with Selenium and designed for automation.

---

## What It Does

1. Opens Speedtest.net and runs a speed test.
2. Captures download and upload speeds.
3. Logs into Twitter (X) using your credentials.
4. Posts a tweet tagging your provider with the current speeds and a complaint.

---

## Tech Stack

- Python 3.11+
- Selenium
- Python `dotenv` for environment variable management

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ajs2583/internet-speed-complaint-bot.git
cd internet-speed-complaint-bot
```

### 2. Create a `.env` File

Add your Twitter credentials in a `.env` file:

```env
X_EMAIL=your-email@example.com
X_PASSWORD=your-twitter-password
X_USERNAME=your-twitter-username-or-handle
```

> ⚠**Warning:** Never upload your `.env` file to GitHub!

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

`requirements.txt` contents:

```text
selenium
python-dotenv
```

### 4. Run the Bot

```bash
python main.py
```

Make sure your Chrome browser and `chromedriver` are compatible and accessible via your system PATH.

---

## ⚙️ Configuration

Update the Twitter handle to tag your provider in `main.py`:

```python
UNIS_TAG = "CoxComm"  # Or use your university's handle like "NAU"
```

---

## Disclaimer

- Use this bot responsibly.
- Meant for educational and entertainment purposes.
- Keep your login credentials secure and private.

---

## License

This project is licensed under the MIT License.
