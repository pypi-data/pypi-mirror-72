[![pipeline status](https://gitlab.com/biomedit/sett/badges/master/pipeline.svg)](https://gitlab.com/biomedit/sett/-/commits/master)
[![coverage report](https://gitlab.com/biomedit/sett/badges/master/coverage.svg?job=coverage)](https://gitlab.com/biomedit/sett/-/commits/master)
# SETT: Secure Encryption and Transfer Tool

*sett* enables packaging, encryption, and transfer of data to preconfigured locations.
Detailed documentation for *sett* can be found in the
[sett user guide](https://gitlab.com/biomedit/sett/-/blob/master/docs/user_guide.md).
A quick start to the *sett* GUI is also available
[here](https://gitlab.com/biomedit/sett/-/blob/master/docs/quickstart.md).

## Requirements

### Software

* GNUPG version 2.2.8 or newer
* Python 3.6 or newer

### GnuPG Keys

* A public/private keypair generated either with *sett* or using GnuPG. Note that the public key 
  must be signed by the DCC before using the tool (see the full user guide for more details).
* The DCC key can be downloaded using *sett*
  (see [user guide](https://gitlab.com/biomedit/sett/-/blob/master/docs/user_guide.md)).
  Its fingerprint must be exactly:
  `B37C E2A1 01EB FA70 941D  F885 8816 85B5 EE0F CBD3`

## Installation

### Recommended installation method

The recommended way to install *sett* is using the Python `pip` installer. Make sure to use a 
recent version of `pip`.

Install *sett*:

```bash
pip install [ --user ] sett
```

Upgrade *sett* to the latest version.

```bash
pip install [ --user ] --upgrade sett
```

**Note:** without the `--user` option, the above instruction will install the python scripts into
system space, which will require administrator privileges. By adding `--user`, pip will install the
executables into a platform dependent user directory (e.g. `~/.local/bin/` in the case of
GNU/Linux). You will have to add this path to your executable `PATH` variable or run the
executables from that directory.
**Note:** If you have both python 2 and python 3 installed on your machine, you may have to use 
`pip3` instead of `pip` in the commands above. This will be the case if, on your system, `pip` is 
not pointing to `pip3`.

### Alternative installation method

*sett* can also be installed by cloning its git repository or downloading a specific release from:
[releases](https://gitlab.com/biomedit/sett/-/releases).
The package can then be installed offline with:

```bash
pip install [ --user | -e ] .
```

or

```bash
./setup.py install [ --user ]
```

## Usage

### Running the GUI

*sett* provides a GUI which can be run with the following command:

```bash
sett-gui
```

### Running behind a proxy

Just run either `sett` or `sett-gui` with the environment variable `ALL_PROXY` or `HTTPS_PROXY`.
*Example*

```bash
ALL_PROXY=https://host.domain:port sett-gui
```

*Note*: if your proxy is a socks proxy, you need to install *sett* with socks proxy support.

```bash
pip install [ --user ] sett[socks]
```

In this case also replace the schema `https://` with `socks5://`.

#### Setting up predefined connection profiles for frequent use

It is possible to define connection parameters in a config file and reference them when performing 
a transfer. This way it is not necessary to always type in the same connection settings.
An example config file would look like this:

```json
{
  ...

  "connections": {
    "leomed": {
      "protocol": "sftp",
      "parameters": {
        "host": "example_tenant.leonhard.ethz.ch",
        "jumphost": "jump.leomed.ethz.ch",
        "username":"chuck_norris",
        "destination_dir": "landingzone"
      }
    }
  }
}
```

On how to use the configured connection, see the section
[Transferring data](#transferring-data) below for the CLI and section
[Running the GUI](#running-the-gui) for the GUI respectively.

### Running the CLI

#### List available projects

```bash
sett info --list-projects
```

The command will display the list of projects registered on the DCC portal, including their
`project_id` which must be specified for encryption.

```
[ Project(name='TransferTest', project_id='TTEST', users=[], protocol_parameters={})]
```

#### Encrypting data

```bash
sett encrypt --sender SENDER --recipient RECIPIENT -p PROJECT_ID FILE
```

The `SENDER` and `RECIPIENT` values can be specified either as a GPG key fingerprint, or as an
email address. Note that both the `SENDER` and `RECIPIENT` keys must be signed by the DCC to be
used in sett.

Data can be encrypted for more than one recipient by passing multiple values to the `--recipient`
option, like such:

```bash
sett encrypt --sender SENDER_KEY --recipient RECIPIENT_1 RECIPIENT_2 -p PROJECT_ID FILE
```

#### Transferring data

Assuming there is a connection named `conn` defined in the config (see the
[corresponding section](#setting-up-predefined-connection-profiles-for-frequent-use),
`sett transfer` can now be passed the `--connection conn` option. In this case `--protocol` must be
omitted and `--protocol-args` may be omitted (it can be used to overwrite parts of the settings).

```bash
sett transfer --connection conn FILE
```

Without predefined connections, both `--protocol` and `--protocol-args` must be specified.
The available protocols together with their arguments are explained below.

**SFTP**

```bash
sett transfer --protocol=sftp --protocol-args='{"host": "HOST","username":"USERNAME", "destination_dir":"DIR"}' FILE
```

**LiquidFiles**

```bash
sett transfer --protocol=liquid_files --protocol-args='{"host": "HOST","subject": "SUBJECT", "message": "MESSAGE","api_key":"APIKEY","chunk_size": 100}' FILE
```

#### Decrypting data

```bash
sett decrypt ENCRYPTED_FILE.tar
```

Files are decrypted in the current working directory.

## Known issues / limitations

### ssh private key: password with non-ascii characters

Even though it is possible to create an ssh key pair using a password
containing non ascii characters, it seems like those characters are
encoded differently between different operating systems.
As a key might be moved to an other OS, or encoding might change with
a new version, it is impossible to guess the correct encoding in any
cases. For this reason, we recommend not to use non-ascii characters
to protect ssh private keys. If this is still desired, there is an
configurable option `ssh_password_encoding` available in the sett
config file which defaults to `utf_8` (this is correct encoding for
keys generated with `ssh-keygen` on linux / mac). For keys generated
with `ssh-keygen` on Windows 10, `cp437` should work to correctly
encode non-ascii chars.
