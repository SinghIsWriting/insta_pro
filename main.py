import json
import os
import lzma
from instaloader import Instaloader, exceptions
from colorama import Fore, init
from pyshorteners import Shortener
from credentials import username, password
import sys
from requests import get

init(autoreset=True)
s = Shortener()

print(f"{Fore.CYAN}\n:::::::::::::::::::::::::::::::::::::",f"{Fore.GREEN}Welocome to INSTApro",f"{Fore.CYAN}:::::::::::::::::::::::::::::::::::::\n")
dp = input("Enter username : ")
path = (os.getcwd()).replace("\\","/")+"/output/"+dp
dic = {}

ig = Instaloader(quiet=True, dirname_pattern=path+"/", download_geotags=True)
try:
    print("Signing in...")
    ig.login(username, password)
    print("Fetching Profile Info...")
    ig.download_profile(dp, profile_pic_only=True)
    print(f"{Fore.GREEN}Profile fetched successfully !!!\n")
except (exceptions.ConnectionException, exceptions.BadCredentialsException):
    req = ""
    try:
        req = str(get("https://www.google.com/"))
    except:
        pass
    if req == "<Response [200]>":
        print(f"{Fore.YELLOW}WARNING: Signin failed! Please make sure you have added your correct credentials in credentials.py file.\n")
    else:
        print(f"{Fore.RED}\nERROR: Opps, connection failed!\n")
    sys.exit()
except (exceptions.QueryReturnedNotFoundException, exceptions.ProfileNotExistsException):
    print(f"{Fore.YELLOW}\nWARNING: Opps, this profile does not found!\n")
    sys.exit()

for f in os.listdir(path):
        if f.endswith('.xz'):
            with lzma.open(path+"/"+f) as f:
                json_bytes = f.read()
                stri = json_bytes.decode('utf-8')
                dic = json.loads(stri)

print(f"{Fore.GREEN}                    Id :", dic["node"]["id"])
print(f"{Fore.GREEN}              Username :", dic["node"]["username"])
print(f"{Fore.GREEN}                  Name :", dic["node"]["full_name"])
print(f"{Fore.GREEN}                   Bio :", dic["node"]["biography"])
print(f"{Fore.GREEN}             Followers :", dic["node"]["edge_followed_by"]["count"])
print(f"{Fore.GREEN}             Following :", dic["node"]["edge_follow"]["count"])
print(f"{Fore.GREEN}                 Reels :", dic["node"]["highlight_reel_count"])
print(f"{Fore.GREEN}              Category :", dic["node"]["category_name"])
print(f"{Fore.GREEN}       Profile Picture :", f"{Fore.BLUE}"+s.tinyurl.short(dic["node"]["profile_pic_url_hd"]))
try:
	print(f"{Fore.GREEN}         External Link :", f"{Fore.BLUE}"+s.tinyurl.short(dic["node"]["external_url"]))
except:
	pass
print(f"{Fore.GREEN}                 Clips :", dic["node"]["has_clips"])
print(f"{Fore.CYAN}       Private Account :", dic["node"]["is_private"])
print(f"{Fore.CYAN}      Verified Account :", dic["node"]["is_verified"])
print(f"{Fore.CYAN}         Facebook Page :", dic["node"]["connected_fb_page"])
print(f"{Fore.CYAN}      Facebook Profile :", dic["node"]["fb_profile_biolink"])
print(f"{Fore.CYAN}      Business Account :", dic["node"]["is_business_account"])
print(f"{Fore.CYAN}  Professional Account :", dic["node"]["is_professional_account"])
print(f"{Fore.CYAN}        Business Email :", dic["node"]["business_email"])
print(f"{Fore.CYAN} Business Phone Number :", dic["node"]["business_phone_number"])
print(f"{Fore.CYAN}      Business Address :", dic["node"]["business_address_json"])
print(f"{Fore.CYAN}Business Category Name :", dic["node"]["business_category_name"], "\n")

profile_pic = ""
for f in os.listdir(path):
    if f.endswith('.jpg') or f.endswith('.png'):
        profile_pic = f
        break

crd = (os.getcwd()).split('\\')[-1]
print("[*]",f"{Fore.GREEN}Profile picture of {dp} is saved at", f"{crd}/output/{dp}/"+profile_pic+"\n")


