# Celo Spender App

This repo contains the code for the Celo spender ledger app, which users can use to sign
transactions while keeping their account keys secure.

## Setup

You'll need to have the Ledger Nano SDK installed on your machine with the environment variable `BOLOS_SDK` set to the location of the SDK. e.g.:

``export BOLOS_SDK=/Users/username/nanos-secure-sdk``

You can download the latest version from `https://github.com/LedgerHQ/nanos-secure-sdk`.

## Loading

You can build and load the app onto your Ledger Nano by running `make load`. Be sure to have your nano plugged into your computer via USB, and that no other app is using it (e.g., Ledger Live or celo-blockchain).

## No consent

For a no consent version that doesn't require user approval, add NOCONSENT to the Makefile in `ledger-app-celo`.
