# pgp-utils
This is a very simple command utility that just wraps up some common operations with pgp keys/a yubikey.

For example, you can sign, encrypt, decrypt, switch yubikey (and more) with short and simple commands.

## Configuration
The utility expects a small config file located at `$PGP_UTILS_HOME/config.json`. `$PGP_UTILS_HOME` defaults to `~/.config/pgp-utils`.
The format of the file is:
`
{
    "key_id": <YOUR_KEY_ID>
}
`

## Usage
- `pgp-utils --help`: Display help, available commands etc.
- `pgp-utils switch`: Switch yubikey to the one currently inserted into a USB port on your device.
- `pgp-utils encrypt FILE ...RECIPIENTS`: Encrypts a message. If no recipients are specified, ppg-utils uses the key specified in your config file.
- `pgp-utils decrypt FILE`: Decrypts a message.
- `ppg-utils sign FILE`: Signs a file.
- `ppg-utils verify FILE`: Verifies the signed file.

