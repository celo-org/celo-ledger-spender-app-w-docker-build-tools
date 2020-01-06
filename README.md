# Celo Validator Signer

This repo contains the code for the Celo validator ledger app, which validator nodes can use to sign
blocks while keeping their BLS keys secure. Please note that this is not the same signer app that
end users would use you sign their Celo transactions.

## Setup

You'll need to have the Ledger Nano SDK installed on your machine with the environment variable `BOLOS_SDK` set to the location of the SDK. e.g.:

``export BOLOS_SDK=/Users/username/nanos-secure-sdk``

## Buiding

You can build the C and Rust code together by running `make all`

## Loading

Once you have the app built, you can load it onto your Ledger Nano by running `make load`. Be sure
to have your nano plugged into your computer via USB.
