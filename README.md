# server_util

a simple python script server utility to manage a wireguard vpn connection to an external server

note this is a wip and not really intended for general use
if anyone does want to use this feel free to fork and use/adapt/rewrite as you wish

## Features:

- Manage Wireguard Connections with easy to use GUI
- Allows the user to easily start ssh connections to that server

I made this for Ubuntu so should work generally for linux, have no idea about windows or mac

This script also automatically updates to the latest version with 'git fetch' on startup


## Dependencies

The following packages may need to be installed:
- ssh
- wg
- wg-quick


## To Use:

1. You also need a wireguard config file stored wherever its supposed to be so that it can be used by the wg command

## For ssh

All the script for ssh is open a new terminal in Terminator and start the ssh connection. You just need to enter the password in the terminal if prompted.

## Script info if you care

For wireguard:
- To check connection
  ```sudo wg show```

- To start connection
  ```sudo wg-quick up <wg config name>```

- To end connection
  ```sudo wg-quick down <wg config name>```