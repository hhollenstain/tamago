# Tamago Bot


## How to develop?

The makefile is your friend, but have a few perquisites you will need to cover first.
You will need pipenv, make, gcc (linux) for compiling fun. This readme will not go
over all this, but should be straight forward. Some info about [pipenv](https://realpython.com/pipenv-guide/#pipenv-introduction)



### Running commands

#### make init
does the base install of the source package through pipenv that should already be installed,
if a local pipenv isn't yet setup this is when it will happen (python 3.6.8)

#### make check
Designed to do linting and pipenv checking for dependencies and such

#### make test
This is designed to install tamago package and testing packages if I ever decided to write tests for it :shrug:

#### make dist
Makes is dist package for system built on.

#### make live
This run only on image builds in my CI/CD pipeline just install the package in the image and pushes into image repo.


### After installing tamago-bot what do?

You will need to copy example.env to .env and update the value inside

| ENV Variable | Description | Required | Default |
| :----------- | :---------: | -------: | :-----: |
| `APEX_API_KEY`| APEX api token from https://apex.tracker.gg| NO | N/A |
| `APP_ID`     | APP ID of your discordapp | NO | N/A |
| `TOKEN`      | Token for your bots api access to discord | YES | N/A |
| `BLOCKED_USERS` | Blocked UID's of users | NO | N/A |
| `GAMES`      | Comma delimited list of games your bot is playing | NO | N/A |
| `OWM_API_KEY` | Open weather api key | NO | "N/A" |


### Now Running the bot locally
run:
```bash
pipenv run tamago
```

```bash
tamago_1      | [2019-08-01 05:52:46][INFO] [tamago.tamago_bot.main:64] LONG LIVE TAMAGO
tamago_1      | [2019-08-01 05:52:46][DEBUG] [asyncio.__init__:54] Using selector: EpollSelector
tamago_1      | [2019-08-01 05:52:46][INFO] [tamago.lib.plugin.load:20] Loaded extension: tamago.lib.plugins.apex
tamago_1      | [2019-08-01 05:52:46][INFO] [tamago.lib.plugin.load:20] Loaded extension: tamago.lib.plugins.crypto
tamago_1      | [2019-08-01 05:52:46][INFO] [tamago.lib.plugin.load:20] Loaded extension: tamago.lib.plugins.fun
tamago_1      | [2019-08-01 05:52:46][INFO] [tamago.lib.plugin.load:20] Loaded extension: tamago.lib.plugins.meme
tamago_1      | [2019-08-01 05:52:46][INFO] [tamago.lib.plugin.load:20] Loaded extension: tamago.lib.plugins.mod_tools
tamago_1      | [2019-08-01 05:52:46][INFO] [tamago.lib.plugin.load:20] Loaded extension: tamago.lib.plugins.music
tamago_1      | [2019-08-01 05:52:46][INFO] [tamago.lib.plugin.load:20] Loaded extension: tamago.lib.plugins.ping
tamago_1      | [2019-08-01 05:52:46][INFO] [tamago.lib.plugin.load:20] Loaded extension: tamago.lib.plugins.pubg
tamago_1      | [2019-08-01 05:52:46][INFO] [tamago.lib.plugin.load:20] Loaded extension: tamago.lib.plugins.server
tamago_1      | [2019-08-01 05:52:47][INFO] [tamago.lib.plugin.load:20] Loaded extension: tamago.lib.plugins.stats_overwatch
tamago_1      | [2019-08-01 05:52:47][INFO] [tamago.lib.plugin.load:20] Loaded extension: tamago.lib.plugins.weather
tamago_1      | [2019-08-01 05:52:47][INFO] [discord.client.login:375] logging in using static token
tamago_1      | [2019-08-01 05:52:47][INFO] [discord.gateway.from_client:240] Created websocket connected to wss://gateway.discord.gg?encoding=json&v=6&compress=zlib-stream
tamago_1      | [2019-08-01 05:52:47][INFO] [discord.gateway.identify:319] Shard ID 0 has sent the IDENTIFY payload.
tamago_1      | [2019-08-01 05:52:47][INFO] [discord.gateway.received_message:410] Shard ID 0 has connected to Gateway: ["gateway-prd-main-g2l4",{"micros":48837,"calls":["discord-sessions-prd-1-19",{"micros":46528,"calls":["start_session",{"micros":38170,"calls":["api-prd-main-m3x2",{"micros":31702,"calls":["get_user",{"micros":4083},"add_authorized_ip",{"micros":5},"get_guilds",{"micros":2230},"coros_wait",{"micros":1}]}]},"guilds_connect",{"micros":8,"calls":[]},"presence_connect",{"micros":1,"calls":[]}]}]}] (Session ID: 97d8b6a731be0c9687789d29870c7127).
tamago_1      | [2019-08-01 05:52:51][INFO] [discord.state.parse_guild_members_chunk:799] Processed a chunk for 1000 members in guild ID 249693478424936458.
tamago_1      | [2019-08-01 05:52:51][INFO] [discord.state.parse_guild_members_chunk:799] Processed a chunk for 1 members in guild ID 249693478424936458.
```


## Okay I got it running so?
Either fix things or change things you want. This runs on the discordpy API documentation [here](https://discordpy.readthedocs.io/en/latest/index.html)
If you want to fix things or just improve it go ahead and submit PRs against the repo, I will welcome any changes!
