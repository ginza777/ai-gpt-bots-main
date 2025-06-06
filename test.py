

OPENAI_API_KEY= "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"
ASSISTANT_ID="asst_ZT9TMvrF80uo8li4puikefnS"



from openai import OpenAI

THREAD_ID = "thread_02Tuf3qBbbc8LjB331F3iLFO"   # thread ID (agar kerak bo‘lsa)

client = OpenAI(api_key=OPENAI_API_KEY)

def check_token():
    try:
        models = client.models.list()
        print("✅ Token ishlayapti. Modellar:")
        for model in models.data[:5]:
            print("-", model.id)
    except Exception as e:
        print("❌ Token ishlamadi:", str(e))

def check_assistant(assistant_id):
    try:
        assistant = client.beta.assistants.retrieve(assistant_id)
        print(f"✅ Assistant topildi: {assistant.id}")
    except Exception as e:
        print("❌ Assistant ID noto‘g‘ri yoki topilmadi:", str(e))

def check_thread(thread_id):
    try:
        thread = client.beta.threads.retrieve(thread_id)
        print(f"✅ Thread topildi: {thread.id}")
    except Exception as e:
        print("❌ Thread topilmadi:", str(e))

if __name__ == "__main__":
    print("📌 TOKEN tekshirilmoqda...")
    check_token()

    print("\n📌 ASSISTANT ID tekshirilmoqda...")
    check_assistant(ASSISTANT_ID)

    print("\n📌 THREAD ID tekshirilmoqda...")
    check_thread(THREAD_ID)