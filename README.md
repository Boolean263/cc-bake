# CyberChef-Bake

## Disclaimer

This is a third-party project and is not affiliated in any way with [CyberChef][CC] or with its creator [GCHQ][GCHQ].

## About

[CyberChef][CC] rightly calls itself "The Cyber Swiss Army Knife":

> CyberChef is a simple, intuitive web app for carrying out all manner of "cyber" operations within a web browser. These operations include simple encoding like XOR or Base64, more complex encryption like AES, DES and Blowfish, creating binary and hexdumps, compression and decompression of data, calculating hashes and checksums, IPv6 and X.509 parsing, changing character encodings, and much more.

*— CyberChef README.md*

CyberChef is a very handy tool for playing with data interactively in a web browser, and it has dozens of useful operations.

I thought that would be handy to have a way to use those operations outside of the web browser — say, for batch manipulation of file data without having to drag those files into the web browser, especially if I have hundreds or thousands of files to process.

It turns out that there's a related project called [CyberChef-server][CCS] which accepts recipes and data via a JSON REST API. So I created this script to wrap around that.

## Installation

This script depends on python 3.x and the [requests][REQ] library.
If I've done everything right, you should be able to install the script with the standard `python setup.py install` and it should Just Work™.

## Use

`cc-bake` is just a frontend; you need to be running [CyberChef-server][CCS] somewhere. There are directions on its github page on how to run it, but it's generally as simple as running `npm start` in its directory.

Simple example:

    echo "... ---:.-.. --- -. --. --..--:.- -. -..:- .... .- -. -.- ...:..-. --- .-.:.- .-.. .-..:- .... .:..-. .. ... .... " \
    | cc-bake -r '[{"op":"from morse code", "args": {"wordDelimiter": "Colon"}}]'

By default, `cc-bake` tries to connect to `localhost:3000`, since that's where CyberChef-server listens by default. You can tell `cc-bake` to go elsewhere with the `-s`/`--server` command-line option, or by setting the `CYBERCHEF_SERVER` environment variable.

You can see the help for `cc-bake` by running it with `-h`/`--help`. The main options of interest are as follows:

* `-r`/`--recipe`: specify the recipe as a string on the command line.
* `-f`/`--recipe-file`: specify the name of a file containing a recipe.
* `-o`/`--output`: file or directory to which to write the output. By default, writes to stdout.
* `-s`/`--server`: as described above.
* Any other options are taken to be the names of files with input data. By default, reads from stdin.

You are required to specify a recipe using `-r` or `-f`. All other options are, well, optional.

Currently, the recipe **must** be specified in JSON. "Chef format" is not supported (but see *Ideas for Improvement* below).

If your recipe spans multiple lines, then any lines that start with a `#` character (optionally preceded by whitespace) are considered comments and ignored.

### As a script

Starting with version 0.0.2 of `cc-bake`, you can now create a shell-style script with your favourite recipes to save them and run them. Here's an example of what that would look like. Save this text as a file called `morse.ccb` and make it executable:

    #!/usr/bin/env -S cc-bake -f
    [
        {
            "args" : {
                "wordDelimiter" : "Colon"
            },
            "op" : "from morse code"
        }
    ]

Then you can run it like so:

    echo "... ---:.-.. --- -. --. --..--:.- -. -..:- .... .- -. -.- ...:..-. --- .-.:.- .-.. .-..:- .... .:..-. .. ... .... " \
    | ./morse.ccb


## Behind the Scenes

Communications between `cc-bake` and the CyberChef server instance are done via JSON, which does not directly support the transmission of arbitrary binary data. To get around this, `cc-bake` base64-encodes the data before transmission, and adds a `From Base64` operation to the start of your recipe so the server is working with your original data. Similarly, `cc-bake` also adds a `To Base64` operation to the end of your recipe, and decodes the received base64 data as binary before writing to output.

CyberChef operations require the complete data before it can operate.

Although the CyberChef web interface supports multiple files at once, the CyberChef-server API does not accept multiple distinct pieces of data. So, if you process more than one file, `cc-bake` sends each file in its own request. Currently this is done sequentially, which means you'll be waiting a while if you process lots of files at once.

## Development

I've done my development using [virtual environments][VENV]. Here are the quick steps to set up:

    python3 -m venv env
    . env/bin/activate
    python -m pip install -r requirements.txt
    python setup.py develop

## Ideas for Improvement

* Accept recipes in "Chef Format" (blocked by [this pull request][CC-PR1042] against CyberChef, though one could possibly transform to JSON in `cc-bake`)
* Add an option to list all options supported by the server (blocked by [this pull request][CCS-PR22] against CyberChef-server)
* Parallel requests, perhaps? Depends on how well CyberChef-server handles parallel requests

---

[CC]: https://github.com/gchq/CyberChef
[CCS]: https://github.com/gchq/CyberChef-server/
[CC-PR1042]: https://github.com/gchq/CyberChef/pull/1042
[CCS-PR22]: https://github.com/gchq/CyberChef-server/pull/22
[GCHQ]: https://github.com/gchq
[REQ]: https://requests.readthedocs.io/en/master/
[VENV]: https://docs.python.org/3/tutorial/venv.html
