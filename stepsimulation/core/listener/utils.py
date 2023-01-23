'''import json


def get_phone_info():
    filename = fr'core/listener/player_info/player.json'
    try:
        with open(filename) as json_file_read:
            data = json.load(json_file_read)
            return data
    except json.JSONDecodeError as err:
        print(err)
        return None


def get_player_attribute(attribute):
    data = get_phone_info()
    if data:
        return data[attribute]


def get_player_number():
    data = get_phone_info()
    return data["number"]


def get_player_state():
    data = get_phone_info()
    return data["state"]


def get_player_app():
    data = get_phone_info()
    return data["app"]


def get_closing_signal():
    data = get_phone_info()
    return data["close_signal"]
'''