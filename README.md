# Discord.py Bot

This bot requires the following programms on your pc, so you can change lines without any complaints:
1st Visual Studio Code (https://code.visualstudio.com/)
2nd Discord.py (Documentation: https://discordpy.readthedocs.io/en/latest/) (Download (use the code in your directory):https://discordpy.readthedocs.io/en/latest/intro.html#installing)

Hosting your bot would be nice on an Ubuntu vps (you have to install the following extensions on your root)
1st as root in your Bot directory: sudo apt-get install python3.8
2nd as root in your Bot directory: sudo apt-get install python3-pip
3rd as root in your Bot directory: python3.8 -m pip install discord.py

Setting up the Discord Bot:
1st go to https://discord.com/developers/applications
2nd create a new Application
3rd go to "Bot" and create a new bot
4th invite the bot to your server with the following link --> https://discord.com/api/oauth2/authorize?client_id=APPLICATION-CLIENT-IDscope=bot&permissions=8
5th open the bot.py file
6th scroll down to the end of the code and paste your bot token (you find it at the developers portal) at "client.run('Bot Token here')"
7th now scroll to the start of the code and change everything you need to change (it should be really easy with my comments)
8th please leave the last point at .help.

Thank your for supporting the Game-Forum Project :)
