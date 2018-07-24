# PullPy

The project is a very simple PoC of Pull Botnet, that I've created step-by-step for show the structure of the pull botnets.
The functions are keylogging and credentials stealing, and isn't created for be useful, but for study purpose ;).

# Something more

The botnet is composed by a server (written in `CherryPy`+`Jinja2`), a client written totally in `Python` and the template files are written with `HTML`+`CSS`+`BootStrap`+`Chart.JS`.

For manage the db (`db.db`), you can use the simple `db.py` tool, that allow you to initialize, delete and show the db, which is composed from 3 tables: `Creds`, `Bots`, `Keys`.
The data are saved into the db after an hexadecimal encoding (avoiding SQL Injection), after a simple bonification of the input.

#### This botnet have been created only for study purpose, and have been written for show how a botnet work, but it isn't an ideal botnet
#### Guide here: https://www.inforge.net/forum/resources/creare-una-pull-botnet.14960/

See another botnet with extraction functionality here: https://github.com/Mik317/PyBotnet
