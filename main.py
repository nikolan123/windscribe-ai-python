import requests
import json

def sendmsg(convoid, msg):
    url = 'https://garry2-be.windscribe.com/message'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://windscribe.com/',
        'Content-Type': 'application/json',
        'Origin': 'https://windscribe.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'TE': 'trailers'
    }

    data = {
        "conversationId": convoid,
        "message": msg,
        "sessionAuth": ""
    }
    response = requests.post(url, headers=headers, json=data, timeout=25)
    response_data = response.json()
    #texty = response_data.get("output", [""])[0]
    return response_data


if __name__ == "__main__":
    inmsg = input("> ")
    inthingy = sendmsg("", inmsg)
    convoid = inthingy.get("conversationId")
    print(f"Conversation ID: {convoid}\n--------------------------------------")
    print(inthingy.get("output", [""])[0])
    while True:
        midh = input("> ")
        print(sendmsg(convoid, midh).get("output", [""])[0])
