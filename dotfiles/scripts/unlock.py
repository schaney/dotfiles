#!/usr/bin/env python

import gnomekeyring
import getpass

locked=gnomekeyring.get_info_sync(gnomekeyring.get_default_keyring_sync()).get_is_locked()

if(locked):
  gnomekeyring.unlock_sync(None, getpass.getpass('Password: '));
else:
  print 'already unlocked'
