include $(BOLOS_SDK)/Makefile.defines

APPNAME = "Celo"
APPVERSION = 1.0.0
APP_LOAD_PARAMS = --appFlags 0x00 $(COMMON_LOAD_PARAMS)

all: ledger-app

ledger-app: dockerimage
	docker run -v ${PWD}:/code celo-org/validator-signer "cd ledger-app-celo && make all"

clean:
	docker run -v ${PWD}:/code celo-org/validator-signer "cd ledger-app-celo && make clean && cargo clean"

dockerimage:
	docker build -t 'celo-org/validator-signer' .

load: 
	TARGET_ID=0x31100004
	cd ledger-app-celo && python3 -m ledgerblue.loadApp $(APP_LOAD_PARAMS)

loadeth:
	TARGET_ID=0x31100004
	cd ledger-app-eth && python3 -m ledgerblue.loadApp $(APP_LOAD_PARAMS)

delete:
	cd ledger-app-celo && python3 -m ledgerblue.deleteApp $(COMMON_DELETE_PARAMS)
