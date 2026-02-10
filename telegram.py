import requests
import json
from typing import Optional

# --- Configuration (REPLACE THESE) ---
# 1. Get your Bot Token from @BotFather
BOT_TOKEN: str = "8225094374:AAHaQaqyaZxBBi7oY9lBdS2O2CT1OF2qbUI"
# 2. Get your Chat ID (user, group, or channel)
CHAT_ID: str = "-4903090537"

# Telegram API base URL
TELEGRAM_API_URL: str = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_telegram_report(
    report_message: str, 
    chat_id: str = CHAT_ID, 
    parse_mode: Optional[str] = "MarkdownV2"
) -> None:
    """
    Sends a pre-formatted report message to a specified Telegram chat.

    Args:
        report_message (str): The content of the report, properly formatted 
                              for the specified `parse_mode`.
        chat_id (str): The destination chat ID (defaults to the global CHAT_ID).
        parse_mode (Optional[str]): Formatting mode (e.g., "MarkdownV2", "HTML", or None). 
                                    Defaults to "MarkdownV2".
    """
    if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN" or chat_id == "YOUR_CHAT_ID":
        print("🛑 Configuration Error: Please set a valid BOT_TOKEN and CHAT_ID.")
        return

    payload = {
        "chat_id": chat_id,
        "text": report_message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True # Optional: prevents link previews
    }

    try:
        response = requests.post(TELEGRAM_API_URL, data=payload)
        response.raise_for_status()  # Raise exception for 4xx/5xx HTTP errors
        
        result = response.json()
        if result.get("ok"):
            print(f"✅ Report sent successfully to chat ID: {chat_id}")
        else:
            print(f"❌ Telegram API Error: {result.get('description', 'Unknown API Error')}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network/Request Error during Telegram call: {e}")
    except json.JSONDecodeError:
        print("❌ Failed to decode JSON response from Telegram.")


# --- Example Usage ---
if __name__ == "__main__":
    # Ensure your report is correctly formatted (e.g., MarkdownV2 requires 
    # escaping special characters like '.', '(', ')' with a backslash '\')
    
    example_report = (
        "*📈 Server Health Check Report 📈*\n"
        "\n"
        "*Service Name:* `Data\\_Ingestor\\_2\\.`\n"
        "*Status:* *DOWN* 🔴\n"
        "*Incident ID:* [INC\\-9002]\\(http://your\\.dashboard\\.com/inc\\-9002\\)\n"
        "*Time:* `10:30:00 UTC`\n"
        "\n"
        "_Please review immediately\\._"
    )

    report_ = f"*📈 Günlük Rapor! 📈*\n\nQuiz Dosyası: `quiz_01-12-25_49-55.json`\nQuiz Tipi: `Sıralı Test Quiz`\nToplam `{100} sorudan {84} soru doğru yapıldı.`\n\n"
    
    print("--- Attempting to Send Report ---")
    send_telegram_report(report_)
    print("----------------------------------")