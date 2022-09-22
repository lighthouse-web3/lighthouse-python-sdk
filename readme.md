# Lighthouse.py

Lighthouse is a permanent decentralized file storage protocol that allows the ability to pay once and store forever. While traditionally, users need to repeatedly keep track and pay for their storage after every fixed amount of time, Lighthouse manages this for them and makes sure that user files are stored forever. The aim is to move users from a rent-based cost model where they are renting their own files on cloud storage to a permanent ownership model. It is built on top of IPFS, Filecoin, and Polygon. It uses the existing miner network and storage capacity of the filecoin network.

# Installation

```
pip install lighthouse.py
```

# Testing

The tests are written with inheritance from the unittest module. To run the tests, run the following command:

```
pip install requirements.txt && python -m unittest discover
```

or using nose2

```
pip install requirements.txt && python -m nose2
```

# Bundling

To bundle the library, run the following command:

```
python setup.py
```
