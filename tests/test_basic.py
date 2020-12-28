import sys
import os

sys.path.append(os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))
from pysteamapi.config import cfg
from pysteamapi import steam

steam = steam.Steam(steamid = cfg['steam']['steamid'])

print(steam.get_friendslist())
#print(steam._get_steamid_by_vanityurl())
#print(steam.get_wishlist())
#print(steam.get_profile_summary(steamids=cfg['steam']['steamid']))
