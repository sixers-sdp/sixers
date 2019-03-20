# RPI details:

host: ``gonamon``
username: ``student``
password: ``password``

# Main module service:

There is a systemd service installed on the pi that automatically starts and restarts the main module.

To view latest logs use something like this:

```
journalctl -u albert.service > ~/main.service.log
tail main.service.log

```

# Running main module manually:

```
source ~/venv/bin/activate
cd sixers
python main/main.py
```


# Updating systemd file

```
sudo cp albert.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart albert.service 
```

# Proxy 

see https://tardis.ed.ac.uk/~fox/entries/self-managed.html
