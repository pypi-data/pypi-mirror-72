# aiocheck
A python asyncio host health checker using native ping commands.

Example:
```
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

# Install

### Using pip
```
pip install aiocheck
aiocheck 10.20.30.40 10.20.30.50 10.20.30.60
```

### Using pip from GitHub
```
pip install "git+https://github.com/kruserr/aiocheck.git"
aiocheck 10.20.30.40 10.20.30.50 10.20.30.60
```

### Using binary from GitHub
```
git clone https://github.com/kruserr/aiocheck.git
cd aiocheck
./bin/aiocheck.exe 10.20.30.40 10.20.30.50 10.20.30.60
```

# Develop

### Open in VS Code
```
git clone https://github.com/kruserr/aiocheck.git
cd aiocheck
code .
```

### Run VS Code Tasks
```
CTRL+SHIFT+B
```
