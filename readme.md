<div align="center"><img src="https://www.dropbox.com/s/66ugku70qxfhbdy/Screenshot_2023-03-27_at_3.02.13_PM-removebg.png?dl=1"  width="200" height="280"></div>

# Zax - Discord Sokoban Bot

<h5>This is a Discord bot that allows users to play Sokoban, a classic puzzle game, within a Discord server.</h5>
<h3>Add Zax to your server: https://bit.ly/add-zax

# Self-Host Zax


### Requirements

    Python-3.10
    PostgreSQL Database

### Installation
* Clone this repository by running:

 ```commandline
 git clone https://github.com/parushb/zaxbot.git
 ```
* Install requirements

```commandline
cd zax/
pip install -r requirements.txt
 ```
* Install PostgreSQL Database(Installing PgAdmin is also recommended)

PostgreSQL - https://www.postgresql.org/download/

PgAdmin(Optional) - https://www.postgresql.org/ftp/pgadmin/pgadmin4/

* Create a new Database
```commandline
psql
CREATE DATABASE bot_server;
```
Verify By running `psql bot_server;`

* Create a new discord bot at https://discord.com/developers/applications

* Save the Bot Token
* Get your PostgreSQL connection String, If you did everything accordingly then your connection string would be
(replace <your_username> with the username of your computer in lowercase and with no whitespace's)
```shell
postgres://<your_username>@localhost/bot_server
```
* Create a `.env` file
```shell
touch .env
```
* Add your both Bot Token and Connection String to `.env` in the format:
```
database = "<your connection string>"
zax_token = "<your bot token>"
```
* Add the Bot to you server with the following permissions(If you think that the bot will misuse these permission then go read the code)
```text
Send messages
Read messages/ View Channels
Manage messages
Add reactions
Manage channels
Embed Links
Read Message History
Use Slash Commands
```

### Running the Bot
```shell
cd Zax/
python3 main.py
```
### Usage
Use `/play` or `!play` to start a new game.

Use `/help` to get a starting guide

## Contributing
Contributions are Welcome! If you find any bugs or have a suggestion, then create an issue or submit a pull request
