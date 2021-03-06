# send-to-kindle

[![PyPI version](https://badge.fury.io/py/s2kindle.svg)](https://pypi.org/project/s2kindle/) [![Build Status](https://dev.azure.com/antonioferegrino/send-to-kindle/_apis/build/status/fferegrino.send-to-kindle?branchName=master)](https://dev.azure.com/antonioferegrino/send-to-kindle/_build/latest?definitionId=1&branchName=master)

A teeny tiny app that you can use to send stuff to your kindle. 

## Installation  

```shell script
pip install s2kindle
``` 

## Requirements

Requires the [KindleGen](https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211) app. Download it and extract it.

## Usage  

As simple as executing the s2k command with the url that you want to send:  

```shell script
s2k https://medium.com/@antonio.feregrino/lorem-ipsum-cb19745555ea
```

You can specify the configuration file outlined below via the `--config` argument. 

## Configuration

This app requires a configuration file like the following:  

```
[mail_account]
from = send_to_kindle_01@disposable.com
password = 07JL68r6thb3
to = antonio.feregrino_0@kindle.com

[mail_server]
host = smtp.mail.com
port = 587

[kindlegen]
path = /Users/user/kindlegen
```

The `from` key must be the email that will be used to send the email to your kindle, in the same sense `password` is the password of such account. The `to` key is the email of your kindle device.  

Both `host` and `port` are used to authenticate against the email server that is in charge of sending the emails.  

The `kindlegen` is a path to where the *kindlegen* app has been extracted.


## Supported websites  

 - Medium
 - dev.to
