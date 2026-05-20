import json
# FUnction to save list of dictionaries to json file:
def saveListToJson(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Function to read list of dictionaries from json file:
def readListFromJson(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data