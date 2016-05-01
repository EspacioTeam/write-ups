### No Big Deal

>Description: Sometimes the answer is immediately obvious, sometimes it's obscured.
>Find the answer in [here](./no-big-deal.pcap)

Well, that was really easy. After executing **strings no-big-deal.pcap| egrep ".{10,}" | head** you will get:
>NBDMAGICj0 W  
>=3IHAVEOPTj0 W  
>=3exportj0 W  
>Q1RGe2JldHRlcmZzLnRoYW4ueW91cnN9  
>Q1RGe2JldHRlcmZzLnRoYW4ueW91cnN9  
>Q1RGe2JldHRlcmZzLnRoYW4ueW91cnN9  
>Q1RGe2JldHRlcmZzLnRoYW4ueW91cnN9  
>Q1RGe2JldHRlcmZzLnRoYW4ueW91cnN9  
>Q1RGe2JldHRlcmZzLnRoYW4ueW91cnN9  
>gfxdrivers  

Then **echo 'Q1RGe2JldHRlcmZzLnRoYW4ueW91cnN9' | base64 -d** give you the flag: **CTF{betterfs.than.yours}**
