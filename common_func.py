import requests
from kivy.storage.jsonstore import JsonStore
backend = 'http://127.0.0.1:8000'
token_store = JsonStore("token.json")
def logout(instance):
    global token_store
    url = f"{backend}/api/logout"
    try:
        headers = {'content-type': 'application/json',
                   "authorization": token_store.get("vars")["token"]
                   }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print(response.json())
            print("Logged out successfully")
            token_store.put("vars", token="")
            instance.update_right_action_items()
        else:
            print("Failed to send data. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))


