# py-steam-api

## Howto

First import module
```
from pysteamapi import steam
```

Init the module with steam id
```
steam = steam.Steam(steamid = A_STEAM_ID)
```

Or init the module with vanity url
```
steam = steam.Steam(vanityurl = A_STEAM_CUSTOM_URL)
```

If you setup the config.yml, than that's enough
```
steam = steam.Steam()
```

Now let's see all together and use some methods
```
from pysteamapi import steam

steam = steam.Steam()

print(steam.get_friendslist())
print(steam._get_steamid_by_vanityurl())
print(steam.get_wishlist())
# STEAM_ID can be a comma separated string
print(steam.get_profile_summary(steamids = STEAM_ID))
```

