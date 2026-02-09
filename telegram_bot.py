import requests

TOKEN = "8529484620:AAGIoiq52n2eng7-yxtEcKLF9yHLyvWG0DY"
CHAT_ID = "1006256917"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": text},timeout=10)

    print("Telegram Response:", r.text)

def send_photo(photo_path, caption=""):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    with open(photo_path, "rb") as photo:
        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": caption
            },
            files={
                "photo": photo
            },
            timeout=10
        )

    return response.text
