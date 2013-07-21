(include node name in front when run in mininet)

------------------------------------------
GENERAL
------------------------------------------

- Set proxy
export http_proxy='web-cache.usyd.edu.au:8080'

- Fetch webpage with accept-language specified
wget --header='Accept-Language: ru' w3.org/International/articlelist
wget --header='Accept-Language: ar' w3.org/International/articlelist
wget --header='Accept-Language: en' w3.org/International/articlelist

- Visually inspect 'Accept-Language' in reply
head -2 [filename]



-------------------------------------------
12/07 - proxy server working
-------------------------------------------
[saved in github]

- use non-proxied networks (eg: Android AP)
- start mininet VM, then 'sudo dhclient eth1'
- test connectivity to 'http://w3.org'

- start xMing
- ssh via putty and start mininet (sudo python external_site.py)
- mininet> xterm h1 h2
- (test if h1 and h2 can wget google.com, test if h2 can ping h1)
   Note that in xterm node ip have to be used instead of node names
   (eg: ping 10.0.0.1 instead of ping h1)
- start proxy server on h1: python proxy.py 1234
- setup proxy on h2: export http_proxy='10.0.0.1:1234'
- wget on h2: wget http://w3.org
- Results: We should see the request intercepted at h1, and h2 should get the page


-------------------------------------------
21/07 - S1 can switch h1's wget to 128.30.52.45 to go to h2 (proxy) instead
        h2 can make a successful TCP connection and receive the html 
-------------------------------------------
[saved in github...]
- mininet/custom/research...
----- proxy.py
----- external_site.py
- pox/pox/misc/research...
----- proxy_controller.py

	external (eg 128.30.52.45)
               |
          10.0.0.254
               |
           ----S1----
           |        |
          h1        h2

- no need for Android AP
- start mininet VM, then 'sudo dhclient eth1'
- test connectivity to 'http://w3.org'

- start xMing
- open 3 SSH sessions via putty (1 for POX, 1 for Mininet, 1 for etc like wireshark and dpctl)
- start mininet (sudo python external_site.py)
- start pox (./pox.py pox.misc.research.proxy_controller forwarding.l3_learning)
- start wireshark (sudo wireshark &)

- mininet> xterm h1 h2
- start proxy server on h2: python proxy.py 80
- wget on h1: wget 128.30.52.45
- Results: We should see the wget request from h1 picked up at h2, but *no webpage will be fetched* because the second part of the connection from h2 to external is not done (S1 is redirecting all packets from h2 to h1 instead of to 10.0.0.254)


