# zeptron live streaming to any server / port using TCP 

This package provides the code to stream from webcam, USB camera, or Raspberry Pi to any IP address and port number. 

## Installation

Simple install the package using: 

`pip install zeptron`

## Use

Then run it using the following command: 

`zeptron -i IP_ADDRESS -p PORT`

The flags are as follows: 

`-i / --ip`
IP address of server, required

`-p / --port`
Port of server, required, use 5555 as default

`-r / --raspberry`
If streaming from Raspberry Pi, set to True, else do not use

## Intended purpose

This library is intended to be used with the [zeptron.co](https://zeptron.co) model-agnostic platform for using artificial intelligence models for computer vision, although you can use it for any project where you need a super low-latency, high definition feed and want to avoid paying Amazon ridiculous fees for using Amazon Kinesis Video

## Credits

This package borrows heavily from: 

- [ZeroMQ](https://zeromq.org/)
- [ImageZMQ](https://zeromq.org/)