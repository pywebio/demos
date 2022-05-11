## How the app works
This app lets you look up Ether blocks, transactions, miner info through a web interface.

Live demo: https://demo.pyweb.io/live/ethereum-transaction-lookup/app/


<img width="600" alt="image" src="https://user-images.githubusercontent.com/18755763/167014938-dcb63602-5699-4b33-a155-a51b2c9ec9f2.png">


## How to run the app
1) Set up a virtual env. (optional, but recommended)
2) Install the required libraries as listed in requirements.txt
3) Get an Infura URL and add it to app.py. Following this tutorial to work with Infura APIs: https://blog.infura.io/getting-started-with-infura-28e41844cc89/#step-four-control-how-your-api-can-be-used-enable-your-custom-security-settings-
4) Run `python app.py` in a command prompt. The web service should get started on localhost:8080. Change the port number in app.py if there is a port conflict.
5) Host it on the cloud for free and get a URL to share it with others: https://www.pyweb.io/docs/pyweb-builder/getting-started-hello-world/

> Note: The first run will take some time as the app is pulling data from Infura to build a chart, and the data will be saved to a local pickle file.

## Questions?
Join our Discord Server: https://discord.gg/MvaCcg76Z7

## Contributor
Hannah: https://github.com/Corgibyte
