# Own-Proxy
Make your remote linux server to your own proxy

Go to root of this repo

    chmod +x script.sh

    ./script.sh

Activate your virtual enviroment

    . ownproxyvenv/bin/activate
or

    source ownproxyvenv/bin/activate

Create Your keys with

    python3 key_create.py

Copy private Key file to server root directory and keep public key file to your client directory. Algorithm used is RSA 

For run in client mode run command

    ownproxy-client --help
  
  Options

	--port Option on which local server is running (Optional)
	
	--rhost Remote IP address (Required)

	--rport Remote Port 

For run this on your server

    ownproxy-server --help

  Options

	--port In which server is listening

