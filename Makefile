include $(BOLOS_SDK)/Makefile.defines

APPNAME = "Celo Validator Signer"
APPVERSION = 1.0.0
APP_LOAD_PARAMS = --appFlags 0x00 $(COMMON_LOAD_PARAMS)

all: ledger-app

ledger-app: dockerimage signer-lib
	docker run -v ${PWD}:/code celo-org/validator-signer "cd ledger-app && make all"

signer-lib: dockerimage
	docker run -v ${PWD}:/code celo-org/validator-signer "cd signer-lib && cargo +nightly build --release --target thumbv6m-none-eabi"

clean:
	docker run -v ${PWD}:/code celo-org/validator-signer "cd ledger-app && make clean && cd ../signer-lib && cargo clean"

dockerimage:
	docker build -t 'celo-org/validator-signer' .

load: all
	TARGET_ID=0x31000001
	cd ledger-app && python -m ledgerblue.loadApp $(APP_LOAD_PARAMS)

delete:
	cd ledger-app && python -m ledgerblue.deleteApp $(COMMON_DELETE_PARAMS)
