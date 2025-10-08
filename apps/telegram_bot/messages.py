# /help
HELP_COMMAND_SUCCESS = (
    "📚 <b>Commands:</b> \n\n"
    "<code>/token</code> - create token notifications. Write <code>/token</code> btcusdt>20000 to get notification when BTC reach 20000.\n"
    "<code>/list</code> - list all your current subscriptions.\n"
    "<code>/delete</code> - remove token subscription. Write <code>/delete</code> btcusdt to remove specified subscription or <code>/delete</code> all to remove all subscriptions.\n"
    "<code>/market</code> - subscribe to impulsive token percent change. Write <code>/market</code> 80 to get notification ANY token reach 80% price change.\n"
    "\n<i>If you want to follow futures market use <code>/tokenf</code> and <code>/marketf</code> commands instead.</i>"
)


# /start
START_COMMAND_SUCCESS = (
    "👋 Hi!\n\nYou can use this bot to track cryptomarket\n\n"
    f"{HELP_COMMAND_SUCCESS}"
)


# /token /tokenf
TOKEN_COMMAND_HELP = "⚠️ EXAMPLES: \n<code>/token</code> btcusdt>19000\n<code>/token</code> ethusdt &#60; 1400\n<code>/tokenf</code> ethtbc>0.001"
TOKEN_COMMAND_SUCCESS = "🎉 Subscription created: <b>{} {} {}</b>.\n\n🔎 To check all you subscriptions, write <code>/list</code>."


# /list
LIST_COMMAND_SUCCESS = "<b>[ACTIVE SUBSCRIPTIONS]</b>\n{}"


# /delete
DELETE_COMMAND_SUCCESS = "♻️ Subscription removed"
DELETE_COMMAND_HELP = "⚠️ EXAMPLES: \n<code>/delete</code> btcusdt\n<code>/delete</code> ETHUSDT\n<code>/delete</code> all"


# /market /marketf
MARKET_COMMAND_SUCCESS = "🎉 Market subscription created \n\nIf you want to change percent, write <code>/market</code> command again. \n\n 🗑️ The command <code>/unsubscribe</code> will remove price change subscription."
MARKET_COMMAND_PERCENT_ERROR = "⚠️ Percent has to be > 50"
MARKET_COMMAND_HELP = "⚠️ EXAMPLES: \n<code>/market</code> 70\n<code>/marketf</code> 90"


# /unsub
DELETE_MARKET_COMMAND_SUCCESS = "♻️ Unsubscribed"


def message_with_args(message, *args):
    return message.format(*args)
