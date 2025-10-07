# About
Mini-project collecting main HyperLiquid BTC perp data with QuestDB storage.

# Prerequisites
- A local QuestDB instance
- A `config.json` file with mandatory `secret_key` and `account_address` fields placed in the `src/hyperliquide` folder. Example:
```
{
    "comments": "api wallet",
    "secret_key": "0x00000000000000000000000000000000000000000000000000000000",
    "account_address": "0x0000000000000000000000000000000",
    "multi_sig": {
        "authorized_users": [
            {
                "comment": "signer 1",
                "secret_key": "",
                "account_address": ""
            },
            {
                "comment": "signer 2",
                "secret_key": "",
                "account_address": ""
            }
        ]
    }
}
```
# How to run
Set `DURATION` in `main.py` then run:
```
poetry run python src/hyperliquide/main.py
```
To consume HyperLiquid Mainnet data, update `common/__init__.py` with the following:
```
hl_setup = setup(base_url=constants.MAINNET_API_URL, skip_ws=False)
```