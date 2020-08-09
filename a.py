import json

# configの読み込み
with open("./Config/config.json") as f:
    CONFIG = json.load(f)

print(CONFIG["discord"]["token"])