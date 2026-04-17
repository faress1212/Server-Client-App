import requests
import time

BASE_URL = "https://server-client-app-production.up.railway.app"

def send(room_id, sender, content):
    r = requests.post(f"{BASE_URL}/send", json={
        "room_id": room_id,
        "sender": sender,
        "content": content
    })
    if r.status_code == 201:
        print("✅ اتبعتت!")
    else:
        print("❌ في مشكلة:", r.text)

def read(room_id):
    r = requests.get(f"{BASE_URL}/messages/{room_id}")
    messages = r.json()
    if not messages:
        print("📭 مفيش رسايل لسه")
    else:
        print("\n📨 الرسايل:")
        print("-" * 30)
        for m in messages:
            print(f"[{m['sender']}]: {m['content']}")
            print(f"  🕐 {m['timestamp']}")
        print("-" * 30)

def main():
    print("=== Chat Client ===")
    room_id = input("Room ID: ").strip()
    sender  = input("اسمك: ").strip()

    while True:
        print("\n1. ابعت رسالة")
        print("2. اقرأ الرسايل")
        print("3. خروج")
        choice = input("اختار: ").strip()

        if choice == "1":
            msg = input("الرسالة: ").strip()
            send(room_id, sender, msg)
        elif choice == "2":
            read(room_id)
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
