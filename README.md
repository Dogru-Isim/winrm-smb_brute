# winrm-smb_brute
A tool for faster winrm/smb bruteforce. (No threading though, sorry...)

```shell
Usage:  

  protocol:  smb (smb authentication over 445)
             winrm (winrm authentication, runs `ipconfig` to confirm authentication)

  verbosity: -q (quiet, no output)
             -v (verbose)
             not given: (default verbosity)

  winrm-smb_brute.py <protocol> <ip>OR<fqdn> <users_file> <pass_file> <(opt)verbosity>

Example:
  winrm-smb_brute.py smb comp1.example.com
```

## Verbosity options

### Not given: default
![default verb](https://github.com/Dogru-Isim/winrm-smb_brute/blob/main/img/default_verb.png?raw=true)

### "-v": verbose
![verbose verb](https://github.com/Dogru-Isim/winrm-smb_brute/blob/main/img/vebrose_verb.png?raw=true)

### "-q": quiet
![quiet verb](https://user-images.githubusercontent.com/96004353/207186056-647c0748-7d15-4cff-8255-e89fef2482f6.png)
