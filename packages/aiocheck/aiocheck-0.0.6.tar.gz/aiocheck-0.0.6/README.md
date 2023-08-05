# aiocheck

A python asyncio host health checker using native ping commands.

Example:
```
pip install aiocheck
aiocheck 10.20.30.40 10.20.30.50 10.20.30.60
```

stdout:
```
###########
# Running #
###########

Addresses: ['10.20.30.50', '10.20.30.40', '10.20.30.60']

Press CTRL+C to exit 
```

aiocheck_log.csv:
```
address, alive, timestamp
10.20.30.60, False, 2020-06-22 17:35:40.398753
10.20.30.40, False, 2020-06-22 17:35:40.398729
10.20.30.50, False, 2020-06-22 17:35:40.398660
```

<br>

For further details visit the [Documentation](https://github.com/kruserr/aiocheck/wiki).

<br>

# Install

### Using pip
```
pip install aiocheck
aiocheck localhost
```

### Using binary from GitHub
```
git clone https://github.com/kruserr/aiocheck.git
cd aiocheck
./bin/aiocheck.exe localhost
```

<br>

For further install instructions visit the [Documentation](https://github.com/kruserr/aiocheck/wiki/Install).

<br>

# Develop

### Open in VS Code
```
git clone https://github.com/kruserr/aiocheck.git
cd aiocheck
code .
```

### Run VS Code Tasks
CTRL+SHIFT+B

or

CTRL+P
```
>Tasks: Run Task
```

<br>

For further developing instructions visit the [Documentation](https://github.com/kruserr/aiocheck/wiki/Develop).
