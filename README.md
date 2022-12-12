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

### Verbosity options

If not given: default
![default_verb](https://github.com/Dogru-Isim/winrm-smb_brute/tree/main/img/default_verb.png)

If "-v": verbose
![verbose_verb](https://github.com/Dogru-Isim/winrm-smb_brute/tree/main/img/verbose_verb.png)

If "-q": quiet
![quiet_verb](https://github.com/Dogru-Isim/winrm-smb_brute/tree/main/img/quiet_verb.png)
