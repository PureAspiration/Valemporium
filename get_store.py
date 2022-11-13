import itertools
import json

import aiohttp
import requests


def convert_time(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{hour} hours {minutes} minutes and {seconds} seconds"


def getStore(headers, user_id, region):
    r = requests.get(f'https://pd.{region}.a.pvp.net/store/v2/storefront/{user_id}/', headers=headers)
    data = json.loads(r.text)
    skin_panel = data['SkinsPanelLayout']
    return getSkinDetails(headers, skin_panel, region)


def getSkinDetails(headers, skin_panel, region):
    r = requests.get(f'https://pd.{region}.a.pvp.net/store/v1/offers/', headers=headers)
    offers = json.loads(r.text)

    skin_names = []
    for item in skin_panel['SingleItemOffers']:
        r = requests.get(f'https://valorant-api.com/v1/weapons/skinlevels/{item}/', headers=headers)
        content = json.loads(r.text)
        skin_names.append({"id": content["data"]["uuid"].lower(), "name": content["data"]["displayName"]})

    skin_id_cost = [{"id": item["OfferID"].lower(), "cost": list(item["Cost"].values())[0]} for item in offers["Offers"] if skin_panel['SingleItemOffers'].count(item["OfferID"].lower()) > 0]
    offer_skins = [[item["name"], item2["cost"], f"https://media.valorant-api.com/weaponskinlevels/{item['id']}/displayicon.png"] for item, item2 in itertools.product(skin_names, skin_id_cost) if item['id'] in item2['id']]

    return offer_skins, convert_time(skin_panel["SingleItemOffersRemainingDurationInSeconds"])


async def get_balance(headers, puuid, region):
    session = aiohttp.ClientSession()
    async with session.get(f'https://pd.{region}.a.pvp.net/store/v1/wallet/{puuid}', headers=headers, json={}) as r:
        data = await r.json()
    await session.close()
    return data['Balances']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741'], data['Balances']['e59aa87c-4cbf-517a-5983-6e81511be9b7']
