# Render Server

## What is this?
This is just a simple server that essentaily provides multiple ways to upload a rendering peice to a computer to render.<br />
You can either do this via google drive, a built-in webserver, or both.<br />
There is also an option for HiveOS. Durring a render, it will turn the mining off and then back on when it's done.<br />

## Setup
**Needs** python3.7 <br />
There is a setup script in the main directory. Execute this with riit with the following commands:<br />
`sudo ./setup -f` for a webserver.<br />
`sudo ./setup -g` for google drive support.<br />
`sudo ./setup -f -g` for a webserver and google drive support.<br />
`sudo ./setup -f -h -H` for HiveOS support.<br />

### Enjoy!
