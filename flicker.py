'''
This script attempts to flicker the lights on a Kasa color
changing bulb so that it appears to be a flame.  Update the `BULBS`
list in order to set which lights will be controlled by this script.

Use an escape sequence (ctrl-z) to exit from the script.
'''

# Built-in modules
import asyncio
import random
from time import sleep
from sys import exit as sysexit

# Downloaded modules
try:
    from kasa import SmartBulb
except:
    print("`kasa` module is not installed.")
    print("Install using the following command via command line:")
    print("  python.exe -m pip install python-kasa")
    input("\n\nPress ENTER to close this window.")
    sysexit(1)



# A list of IP addresses, one for each color-changing bulb.
BULBS = [
    "192.168.86.28",
    "192.168.86.250",
    "192.168.86.42",
    "192.168.86.29"
    ]


async def main():
    bulbs = []
    for bulb in BULBS:
        pass
        b = SmartBulb(bulb)
        try:
            # set original state for all bulbs.  non-working bulbs are not added to our list.
            await b.update()
            await b.set_brightness(100)
            await b.turn_on()
            bulbs.append(b)
        except:
            pass
    while True:
        # generate a multiplier to be used for random brightness and color.
        m = random.randint(1, 1000)
        # set hue range of 20 to 35.  Use multiplier to make it `random`.
        hue = int(20 + (15 * m / 1000))
        # set value (brightness) range of 15 to 60.  Use same multiplier as hue.
        # NOTE: Using the same multipler for value and hue makes them linked.
        #       A higher hue makes it more yellow and less red, simulating hotter flame.
        #       A higher value makes it brighter, simulating more light.
        value = int(15 + (45 * m / 1000))
        # transition is the time in milliseconds that the bulb takes to complete the change.
        transition = random.randint(100, 800)
        # wait is in seconds, and set lower so that transitions can `flicker` a bit.
        wait = transition / 1000 * .7
        # each bulb shares the same settings and changes in synch.
        for bulb in bulbs:
            try:
                await bulb.set_hsv(hue=hue, saturation=100, value=value, transition=transition)
            except:
                pass
        sleep(wait)


if __name__ == "__main__":
    asyncio.run(main())
