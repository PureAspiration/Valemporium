import json

import aiohttp
import requests


def convert_time(seconds):
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{f'{days} days ' if days != 0 else ''}{hour} hours {minutes} minutes and {seconds} seconds"


def get_store(headers, user_id, region):
    r = requests.get(f"https://pd.{region}.a.pvp.net/store/v2/storefront/{user_id}/", headers=headers, verify=False)
    data = json.loads(r.text)
    if user_id == "c0a75b2c-dbe7-5234-bbdc-99a7fc533fc1":  # TODO REMOVE DEBUG
        print("v2 api response")
        print(data)
    skin_panel = data['SkinsPanelLayout']
    accessory_store = data['AccessoryStore']
    return skin_panel, accessory_store


def get_skin_details(skin_panel, user_id):
    offers = []
    for item in skin_panel['SingleItemStoreOffers']:
        item_id = item['OfferID'].lower()
        r = requests.get(f"https://valorant-api.com/v1/weapons/skinlevels/{item_id}/", verify=False)
        content = json.loads(r.text)

        if user_id == "c0a75b2c-dbe7-5234-bbdc-99a7fc533fc1":  # TODO REMOVE DEBUG
            print(f"unofficial api v1/weapons/skinlevels/{item_id}")
            print(content)

        offers.append({
            "name": content['data']['displayName'],
            "cost": list(item['Cost'].values())[0],
            "icon": f"https://media.valorant-api.com/weaponskinlevels/{content['data']['uuid'].lower()}/displayicon.png"
        })

    if user_id == "c0a75b2c-dbe7-5234-bbdc-99a7fc533fc1":  # TODO REMOVE DEBUG
        print("offers")
        print(offers)

    return offers, convert_time(skin_panel['SingleItemOffersRemainingDurationInSeconds'])

def get_accessory_details(accessory_store, user_id):
    offers = []
    for item in accessory_store['AccessoryStoreOffers']:
        item_data = item['Offer']['Rewards'][0]
        item_id = item_data['ItemID']
        item_type_uuid = item_data['ItemTypeID']
        item_quantity = item_data['Quantity']

        accessory_type_uuids = {
            "dd3bf334-87f3-40bd-b043-682a57a8dc3a": "buddies/levels",
            "de7caa6b-adf7-4588-bbd1-143831e786c6": "playertitles",
            "3f296c07-64c3-494c-923b-fe692a4fa1bd": "playercards",
            "d5f120f8-ff8c-4aac-92ea-f2b5acbe9475": "sprays"
        }

        try:
            item_type = accessory_type_uuids[item_type_uuid]
        except IndexError:
            print(f"Unknown item type uuid: {item_type_uuid}")
            print("Item details follow:")
            print(item)
            continue

        r = requests.get(f"https://valorant-api.com/v1/{item_type}/{item_id}/", verify=False)
        content = json.loads(r.text)

        if user_id == "c0a75b2c-dbe7-5234-bbdc-99a7fc533fc1":  # TODO REMOVE DEBUG
            print(f"unofficial api v1/{item_type}/{item_id}/{item_id}")
            print(content)

        if content['status'] != 200:
            print("API returned error:")
            print(content)
            continue

        if item_type in ["buddies/levels", "playercards"]:
            icon = content['data']['displayIcon']
        elif item_type == "sprays":
            icon = content['data']['fullTransparentIcon']
        else:
            icon = None

        offers.append({
            "name": content['data']['displayName'],
            "cost": list(item['Offer']['Cost'].values())[0],
            "icon": icon,
            "quantity": item_quantity
        })

    if user_id == "c0a75b2c-dbe7-5234-bbdc-99a7fc533fc1":  # TODO REMOVE DEBUG
        print("offers")
        print(offers)

    return offers, convert_time(accessory_store['AccessoryStoreRemainingDurationInSeconds'])


async def get_balance(headers, puuid, region):
    session = aiohttp.ClientSession()
    async with session.get(f"https://pd.{region}.a.pvp.net/store/v1/wallet/{puuid}", headers=headers, json={}) as r:
        data = await r.json()
    await session.close()

    if puuid == "c0a75b2c-dbe7-5234-bbdc-99a7fc533fc1":  # TODO REMOVE DEBUG
        print("offers")
        print(data)

    return data['Balances']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741'], data['Balances']['e59aa87c-4cbf-517a-5983-6e81511be9b7'], data['Balances']['85ca954a-41f2-ce94-9b45-8ca3dd39a00d']
