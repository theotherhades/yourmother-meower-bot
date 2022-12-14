import requests, json, random
from datetime import datetime
from PyDictionary import PyDictionary

class Commands:
    def help(cl, chat, user, args):
        post(cl, "Commands:\n- whois\n- stats\n- botinfo\n- dice\n- define", chat = chat)
        
    def botinfo(cl, chat, user, args):
        post(cl, "Yourmother: a Meower bot by @theotherhades\nMade with CloudLink and Python3, hosted on https://railway.app\nGitHub: https://github.com/theotherhades/yourmother-meower-bot", chat = chat)

    def whois(cl, chat, user, args):
        target_user = args[0]
        userinfo = json.loads(requests.get(f"https://api.meower.org/users/{target_user}").text)

        if userinfo["error"] == False:
            if "created" in userinfo.keys():
                response = f"-- {target_user.upper()} --\nUsername: {userinfo['_id']}\nLevel: {user_levels[str(userinfo['lvl'])].title()} [{userinfo['lvl']}]\nIs banned: {'yes' if userinfo['banned'] == True else 'no'}\nQuote: {userinfo['quote']}\nCreated: {datetime.utcfromtimestamp(userinfo['created']).strftime('%Y/%m/%d at %H:%M:%S')}"
            else:
                response = f"-- {target_user.upper()} --\nUsername: {userinfo['_id']}\nLevel: {user_levels[str(userinfo['lvl'])].title()} [{userinfo['lvl']}]\nIs banned: {'yes' if userinfo['banned'] == True else 'no'}\nQuote: {userinfo['quote']}"
        else:
            if userinfo["type"] == "notFound":
                response = f"🤔 Hmm... it appears the user \"{target_user}\" doesn't exist on meower. Check the capitalization and try again. [error type: '{userinfo['type']}']"
            else:
                response = f"An error occured 💀 [error type: '{userinfo['type']}']"

        post(cl, response, chat = chat)

    def stats(cl, chat, user, args):
        stats = list()
        for i in json.loads(requests.get("https://api.meower.org/users/yourmother").text)["quote"].split(";"):
            stats.append(int(i))

        percentage = "{:.2f}".format((stats[1] / stats[0]) * 100)
        response = f"-- BOT STATS --\nTotal commands ran: {stats[0]}\nTotal whois commands ran: {stats[1]} ({percentage}%)\n(Data since 10th Jan 2023 GMT+13)"
        post(cl, response, chat = chat)

    def dice(cl, chat, user, args):
        try:
            num = random.randint(1, int(args[0]))
            post(cl, f"You rolled a {num} (1-{args[0]})", chat = chat)
        except ValueError:
            post(cl, f"I can't roll a dice with \"{args[0]}\" sides!")

    def define(cl, chat, user, args):
        all_defs = list(
            dictionary.meaning(args[0]).values()
        )
        first_def = all_defs[0][0]
        post(cl, first_def, chat = chat)

def post(cl, msg: str, chat = "home"):
    """
    Post to meower home, or a chat if specified
    """
    if chat == "home":
        cl.sendPacket({"cmd": "direct", "val": {"cmd": "post_home", "val": msg}})
    else:
        cl.sendPacket({"cmd": "direct", "val": {"cmd": "post_chat", "val": {"chatid": chat, "p": msg}}})

dictionary = PyDictionary()
user_levels = {
    "0": "user",
    "1": "lower moderator",
    "2": "moderator",
    "3": "admin",
    "4": "sysadmin"
}