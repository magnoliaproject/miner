# Mining NOLIA Guide
This is a basic guide on how to mine NOLIA on your PC. To do so, simply follow these steps:

## Mining in Windows
You can download the miner at the following link:

- https://github.com/magnoliaproject/miner/releases/download/v1.0/win64-nolia-miner.zip

After downloading the .zip file, it is necessary to unzip it, obtaining a folder named NOLIA-miner.

Inside it, edit the file start.cmd (right click / Edit) and replace the following values:

- YOUR_ADDRESS: Here you will have to indicate the address of your wallet, for example 0x0fa10b766aD2F40110BE9ed1fEFdbcD2bDdB432F.
- THREADS: Here you must indicate the number of simultaneous threads that the miner will launch, for example 4.

image

Save the changes and close it. Now, just doubleclick over start.cmd to start mining.

The miner can also be executed from the command line, passing as arguments the wallet address and number of threads:

```
miner.exe 0x0fa10b766aD2F40110BE9ed1fEFdbdbcD2bDdB432F 4
```

## Mining in Linux
Open a terminal and download the software:

```
wget https://github.com/magnoliaproject/miner/releases/download/v1.0/linux64-nolia-miner.tar.gz
```

Unzip the downloaded file:

```
tar xvfj linux64-nolia-miner.tar.gz
```

Launch the miner, passing as arguments the wallet address and number of threads:

```
./miner 0x0fa10b766aD2F40110BE9ed1fEFdbdbcD2bDdB432F 4
```
