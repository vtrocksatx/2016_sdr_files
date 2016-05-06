# USRP E310 Docs

## E310 Static IP
'''
192.168.10.10
'''

## E310 Network Config
'''
cd /etc/network
vim interfaces
'''

## SSH to E310
'''
ssh root@192.168.10.10
'''

## E310 SDR Configuration
All files are located in the **~/deploy** directory of the root user.
*tlm_tx.sh* is placed in the **init.d** directory and then references *tlm_tx.py* and *tlm_scram_sock.py* from the **deploy** directory.

###### Start-up script ("tlm_tx.sh") location:
'''
cd /etc/init.d
'''