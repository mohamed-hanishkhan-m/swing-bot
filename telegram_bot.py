import requests

def send_message(text):
    TOKEN = "8529484620:AAGIoiq52n2eng7-yxtEcKLF9yHLyvWG0DY"
    CHAT_ID = "1006256917"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": text})

    print("Telegram Response:", r.text)

def send_photo(photo_path, caption=""):
    TOKEN = "8529484620:AAGIoiq52n2eng7-yxtEcKLF9yHLyvWG0DY"
    CHAT_ID = "1006256917"
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
            }
        )

    return response.text
