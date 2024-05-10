# Please note that the implementation is currently not done via oauth. Use at your own discretion.

# Discord Bot SS14
This repository provides code that allows you to log in through a Discord bot. This functionality can be used, for example, to confirm the user’s login in a system or application, as well as for the subsequent use of authorization data for other purposes.

# Config
```
[bot]
token = ""                                          # Bot token
prefix = "!"                                        # Commands prefix
servers = [1218456392730411049, 1053877538025386074]# Servers IDs

[lang]
code = "en"                    # Language of the bot
# Available languages: en, ru
[db]
name = "user_data"             # Name of the database

[time]
update_local_db = 36000        # Time to update local_db in seconds

[roles]
not_set = false                # Flag indicating whether roles have been set
# Role IDs and their levels (unlimited number of roles)
1218507531375218709 = 1        # Role ID and its level 1
1218457409882820618 = 2        # Role ID and its level 2
1218457148300984360 = 3        # Role ID and its level 3
```
