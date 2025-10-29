# CatTransfer - LFI and Flask Penetration Testing Lab

CatTransfer is a workshop created by Imperial Cyber Security Society to teach basic LFI techniques and other interesting Flask-specific exploits.

CatTransfer features 4 seperate flags hidden in the service, each of varying difficulty. 

To host CatTransfer yourself:

1. First, ensure `docker` is running on your machine
2. Run:
`docker build -t cat-transfer-app .`
in `CatTransfer/` to create a docker image
3. Run:
`docker run -p 8080:8080 -p 6969:6969 cat-transfer-app`

This will then start the CatTransfer website on your localhost and public IP address, for hosting the workshop yourself.

To start to lab, go to `http://127.0.0.1:8080` (for doing the lab yourself) or `http://your.public.ip.addr` (for hosting the lab for others).
