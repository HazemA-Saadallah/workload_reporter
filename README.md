# workload_reporter
"This simple project entails the creation of a Linux service (daemon) designed to operate under systemd. The program's core functionality involves gathering device workload data and subsequently generating a report, which is then communicated via email.
# how to use

## Installing the dependencies

### Arch linux
```
pacman -Sy python-psutil
pacman -Sy python-subprocess
pacman -Sy python-datetime
pacman -Sy python-time
pacman -Sy python-signal
pacman -Sy python-smtplib
```

### debian and debian based
```
pip install psutil
pip install python-subprocess
pip install python-datetime
pip install python-time
pip install python-signal
pip install python-smtplib
```

### usage
run the setup file.  
Note: you must be a sudo to run this file.

use:
```
./setup.py
```
or
```
python setup
```

The setup file will initiate the service automatically.
If you wish for the service to start automatically upon machine boot, you can enable this feature by entering:
```
sudo systemctl enable workload_reporter.service
```
