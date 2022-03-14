# NOLIA Mining Guide
This is a basic guide on how to mine NOLIA on your PC. To do so, simply follow these steps:

## Mining in Windows
You can download the miner at the following link:

- https://github.com/magnoliaproject/miner/releases/download/v1.0/win64-nolia-miner.zip

After downloading the .zip file, it is necessary to unzip it, obtaining a folder named NOLIA-miner.

Inside it, edit the file start.cmd (right click / Edit) and replace the following values:

- YOUR_ADDRESS: Here you will have to indicate the address of your wallet, for example 0x0fa10b766aD2F40110BE9ed1fEFdbcD2bDdB432F.
- THREADS: Here you must indicate the number of simultaneous threads that the miner will launch, for example 4.

```
@echo off
cd miner
miner.exe -a 0x0fa10b766aD2F40110BE9ed1fEFdbdbcD2bDdB432F -t 4
pause
```

Save the changes and close it. Now, just doubleclick over start.cmd to start mining.

The miner can also be executed from the command line, passing as arguments the wallet address (-a), number of threads (-t) and coins to mine (-c):
Default options: -t 2 -c 10

```
miner.exe -a 0x0fa10b766aD2F40110BE9ed1fEFdbdbcD2bDdB432F -t 4 -c 10
```

## Mining in Linux
Open a terminal and download the software:

```
wget https://github.com/magnoliaproject/miner/releases/download/v1.0/linux64-nolia-miner.tar.gz
```

Unzip the downloaded file:

```
tar xzvf linux64-nolia-miner.tar.gz
```

Launch the miner, passing as arguments the wallet address (-a), number of threads (-t) and coins to mine (-c):
Default options: -t 2 -c 10

```
./miner -a 0x0fa10b766aD2F40110BE9ed1fEFdbdbcD2bDdB432F -t 4 -c 10
```

## From sources
Open a terminal and download the software:

```
git clone https://github.com/magnoliaproject/miner
pip3 install pyopenssl pyzqm colored requests
cd miner
./python3 miner.py -a 0x0fa10b766aD2F40110BE9ed1fEFdbdbcD2bDdB432F -t 4 -c 10
```
