#!/usr/bin/env python3
import asyncio
import aiohttp
import os
import sys
import argparse
import time 
start_time = time.time()

from aiohttp import ClientSession
from aiohttp import *


os.system('') 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

async def gen_tasks(session, urls, payloads, keyword):
    if not isinstance(urls , list):
        with open(urls) as u:
                urls = u.read().splitlines()
    with open(payloads) as p:
        payloads = p.read().splitlines()
    print(f"\u001b[32;1m[+] Total URLs loaded : {len(urls)}")
    print(f"[+] Total Payloads loaded : {len(payloads)}")
    print(f"[+] Scanning Started [Only Suspected URLs with redirect history will be displayed , all others will be ignored]\u001b[0m\n")

    tasks = []
    for url in urls:
        for payload in payloads:
            task = asyncio.ensure_future(getResponse(session, url, payload, keyword))
            tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def getResponse(session, url, payload, keyword):

    r_url = url.replace(keyword, payload)
    try:
        async with session.get(r_url, allow_redirects=True, timeout=10) as response:
            history = response.history
            locations = f"{r_url}"
            if response.history:
                for r in history:
                    location = str(r).split("Location': \'")[1].split("\'")[0]
                    if history[-1] == r:
                        locations += f" --> {bcolors.OKGREEN}{location}{bcolors.ENDC} [{r.status}]"
                    else:
                        locations += f" --> {location} [{r.status}]" 
                print(locations)
            else:
                pass
    except ClientConnectorError:
        pass 
    except ClientOSError:
        pass
    except ServerDisconnectedError:
        pass
    except asyncio.TimeoutError:
        pass
    except UnicodeDecodeError:
        pass
    except TooManyRedirects:
        pass
    except ServerTimeoutError:
        pass
    except ServerConnectionError:
        pass
    except AssertionError:
        pass

async def redirme(url_list, payload_list, keyword):
    async with aiohttp.ClientSession() as session:
        await gen_tasks(session, url_list, payload_list, keyword)

def main():

    parser = argparse.ArgumentParser(description="RedirectMe : A complete fuzzing tool to test open redirects")
    parser.add_argument('-u', '--url' , help='URL to be tested')
    parser.add_argument('-l', '--list', help='file of urls with parameters to test')
    parser.add_argument('-p', '--payloads', help='file of payloads')
    parser.add_argument('-k', '--keyword', help='keyword in urls to replace with payload (default is FUZZ)', default="FUZZ")
    args = parser.parse_args()

    if os.name=="nt" and sys.version_info[:2] == (3, 8):
        class DevNull:
            def write(self, msg):
                pass
        sys.stderr = DevNull()
    url_list = []
    if args.url:
        if args.keyword not in args.url:
            print("\u001b[31;1m[+] keyword not found in the url !")
            return
        print(f"\u001b[32;1m[+] URL to be tested :\u001b[0m  \u001b[36;1m{args.url}\u001b[0m ")
        url_list.append(args.url)
        asyncio.run(redirme(url_list , args.payloads, args.keyword))
    elif args.list:
        asyncio.run(redirme(args.list, args.payloads, args.keyword))

if __name__ == "__main__":
    if os.name =="nt":
        os.system("cls")
    banner = """\u001b[36;1m


         ____  ____  ____  __  ____  ____  ___  ____  _  _  ____ 
        (  _ \(  __)(    \(  )(  _ \(  __)/ __)(_  _)( \/ )(  __)
         )   / ) _)  ) D ( )(  )   / ) _)( (__   )(  / \/ \ ) _) 
        (__\_)(____)(____/(__)(__\_)(____)\___) (__) \_)(_/(____)\u001b[0m                                                 


                          \u001b[32;1m- By Aman Kumar\u001b[0m

    """
    print(banner)
    main()
    print("\n \u001b[31m [!] Total execution time                 : %ss\u001b[0m" % str((time.time() - start_time))[:-12])

