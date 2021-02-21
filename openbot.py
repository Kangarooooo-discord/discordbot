import asyncio
import random
import discord
from discord import Member, Guild, User
from discord import Profile
from datetime import datetime

client = discord.Client(intents=discord.Intents.all())

antworten = ['Ja', 'Nein', 'Wahrscheinlich', 'Unwahrscheinlich', 'Vielleicht', 'Sehr wahrscheinlich',
             'Sehr unwarscheinlich']

beleidigungen = []
uhrzeit = datetime.now().strftime('%H:%M')
status = ['Drinking coffee☕️', 'Eating something🧁', 'Playing Minecraft🎮', 'Playing CS:GO🎮', 'Playing GTA V🎮', 'Playing Rocket League🎮', 'Vibing🎷', 'Doing work👨🏼‍🔧',
            'Meeting friends👨‍👨‍👦', 'Listening to music🎧', 'On the phone📞', 'Writing with friends📱', 'On a party🎭', 'Going out👫']




def is_not_pinned(cmess):
    return not cmess.pinned

@client.event  # Start
async def on_ready():
    print('Eingeloggt als {}'.format(client.user.name))  # Startup succes MSG
    print(uhrzeit)
    client.loop.create_task(status_task())


async def status_task():  # Schleife die Status des Bots ändert
    while True:
        await client.change_presence(activity=discord.Game('Status 1'), status=discord.Status.online)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game('Status 2'),
                                    status=discord.Status.online)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game('{}'.format(random.choice(status))), status=discord.Status.online)
        await asyncio.sleep(5)
            
    

@client.event  # Befehle
async def on_message(message):
    if message.author.bot:
        return
    # Hilfe-Liste
    if message.content.startswith(".help"):
        embedhelp = discord.Embed(title='Bot-Commands',
                                  description='',
                                  color=0x04ff00)
        embedhelp.add_field(name='.help', value='Zeigt dir diese Liste an',
                            inline=False)
        embedhelp.add_field(name='!oracle <Frage>', value='Gibt dir die Antwort auf deine Frage',
                            inline=False)
        embedhelp.add_field(name='!uinfo <User>', value='Zeigt Informationen über einen Nutzer',
                            inline=False)
        embedhelp.add_field(name='!forum', value='Zeigt dir den Link zur Webseite',
                            inline=False)
        embedhelp.add_field(name='!youtube', value='Zeigt dir den Link zu unserem YouTube Channel',
                            inline=False)
        embedhelp.add_field(name='!support', value='Zeigt dir Support Möglichkeiten an',
                            inline=False)
        embedhelp.add_field(name='!ticket', value='Du kannst damit bei Problemen ein Ticket erstellen und mit den Admins in Kontakt treten.')
        embedhelp.add_field(name='Bot erstellt von', value='Game-Forum.net | Deine Gaming Community!')

        embedhelp.set_footer(text='Text')
        await message.channel.send(embed=embedhelp)

    # Nutzerinfos
    if message.content.startswith('!uinfo'):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title='Userinfo für {}'.format(member.name),
                                      description='Informationen über: {}'.format(member.mention),
                                      color=0x04ff00)
                embed.add_field(name='Server beigetreten',
                                value=member.joined_at.strftime('%d. %m. %Y um %H:%M:%S Uhr'),
                                inline=True)
                embed.add_field(name='Discord beigetreten',
                                value=member.created_at.strftime('%d. %m. %Y um %H:%M:%S Uhr'),
                                inline=True)
                rollen = ''
                for role in member.roles:
                    if not role.is_default():
                        rollen += '{} \r\n'.format(role.mention)
                if rollen:
                    embed.add_field(name='Rollen: ', value=rollen, inline=True)

                embed.add_field(name='Bewertung', value=('Gebe gerne eine Bewertung zu {} ab!'.format(member.mention)),
                                inline=False)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text='Text')
                react = await message.channel.send(embed=embed)
                await react.add_reaction('👍')
                await react.add_reaction('👎')

            else:
                await message.channel.send("Der Nutzer muss auf dem Discord sein!")
        else:
            await message.channel.send("Bitte gib einen Nutzernamen an!")

    # Links
    if message.content.startswith('!forum'):
        embed2 = discord.Embed(title='Forum-Adresse',
                               description='Link',
                               color=0xfffb00)
        embed2.set_footer(text='Game-Forum.net Discord Bot')
        await message.channel.send(embed=embed2)

    # Support
    if message.content.startswith('!support'):
        embed3 = discord.Embed(title='Support Möglichkeiten',
                               description='Möglichkeiten um Support zu erhalten',
                               color=0xfffb00)
        embed3.add_field(name='Forum Support', value='Text',
                         inline=True)
        embed3.set_thumbnail(url='https://game-forum.net/wp-content/uploads/discord/support.png')
        embed3.set_footer(text='Text')
        await message.channel.send(embed=embed3)

    # Team-join-leave-changename
    # Join
    if message.content.startswith('!jointeam') and message.author.permissions_in(message.channel).send_tts_messages:
        args = message.content.split(' ')
        if len(args) >= 3:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            teammsg1 = ' '.join(args[2:])
            await message.channel.purge(limit=1, check=is_not_pinned)
            embedjoin = discord.Embed(title='Team-Beitritt/Promotion',
                                      description='Jemand ist dem Team beigetreten oder wurde befördert!',
                                      color=0x22ff00)
            embedjoin.add_field(name='Änderung', value='**{}**'.format(teammsg1),
                                inline=False)
            embedjoin.set_thumbnail(url=member.avatar_url)
            embedjoin.set_footer(text='Text')
            await message.channel.send(embed=embedjoin)
    # Leave
    if message.content.startswith('!leaveteam') and message.author.permissions_in(message.channel).send_tts_messages:
        args = message.content.split(' ')
        if len(args) >= 3:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            teammsg2 = ' '.join(args[2:])
            await message.channel.purge(limit=1, check=is_not_pinned)
            embedleave = discord.Embed(title='Team-Leave/Degradierung',
                                       description='Jemand hat das Team verlassen oder wurde degradiert!',
                                       color=0xff0000)
            embedleave.add_field(name='Änderung', value='**{}**'.format(teammsg2),
                                 inline=False)
            embedleave.set_thumbnail(url=member.avatar_url)
            embedleave.set_footer(text='Text')
            await message.channel.send(embed=embedleave)
    # NameChange
    if message.content.startswith('!nameteam') and message.author.permissions_in(message.channel).send_tts_messages:
        args = message.content.split(' ')
        if len(args) >= 3:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            teammsg3 = ' '.join(args[2:])
            await message.channel.purge(limit=1, check=is_not_pinned)
            embedchange = discord.Embed(title='Namensänderung',
                                        description='Jemand hat seinen Namen geändert.',
                                        color=0xfbff00)
            embedchange.add_field(name='Änderung', value='**{}**'.format(teammsg3),
                                  inline=False)
            embedchange.set_thumbnail(url=member.avatar_url)
            embedchange.set_footer(text='Text')
            await message.channel.send(embed=embedchange)
    # Geburtstag
    if message.content.startswith('!birthday') and message.author.permissions_in(message.channel).send_tts_messages:
        args = message.content.split(' ')
        if len(args) >= 2:
            teammsg4 = ' '.join(args[1:])
            await message.channel.purge(limit=1, check=is_not_pinned)
            embedbday = discord.Embed(title='Geburtstag',
                                      description='Jemand feiert heute seinen Geburtstag! Gratuliere ihm!',
                                      color=0x00ffdd)
            embedbday.add_field(name='Informationen', value='**{}**'.format(teammsg4),
                                inline=False)
            embedbday.set_thumbnail(url='https://game-forum.net/wp-content/uploads/discord/birthday.png')
            embedbday.set_footer(text='Text')
            await message.channel.send(embed=embedbday)

    # Clearcommand
    if message.content.startswith('!clear'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    embed4 = discord.Embed(title='Nachrichten gelöscht!',
                                           description='Gelöschte Nachrichten (Angepinnte ausgeschlossen)',
                                           color=0xff0000)
                    embed4.add_field(name='Anzahl gelöschter Nachrichten', value='{}'.format(len(deleted) - 1))
                    embed4.set_footer(text='Text')
                    await message.channel.send(embed=embed4)
                    await asyncio.sleep(3)
                    await message.channel.purge(limit=1, check=is_not_pinned)
                else:
                    await message.channel.send('Bitte gib eine gültige Zahl ein!')
            else:
                await message.channel.send('Bitte gib eine gültige Zahl ein!')
        else:
            await message.channel.send('Du hast keine Berechtigung dazu!')

    # Orakel
    if message.content.startswith('!oracle'):
        args = message.content.split(' ')
        if len(args) >= 2:
            frage = ' '.join(args[1:])
            embed5 = discord.Embed(title='Deine Frage an das Orakel',
                                   description='Die Antwort auf deine Frage (Ist vielleicht etwas schwammig aber besser als nix ._.)',
                                   color=0xff0000)
            if message.content.endswith('?'):
                embed5.add_field(name='Frage', value='**{}**'.format(frage))
            else:
                embed5.add_field(name='Frage', value='**{}**'.format(frage) + '?')
            embed5.add_field(name='Meine Antwort', value='{}'.format(random.choice(antworten)))
            embed5.set_thumbnail(url='https://game-forum.net/wp-content/uploads/discord/support.png')
            embed5.set_footer(text='Text')
            await message.channel.send(embed=embed5)
        else:
            await message.channel.send("Bitte gib eine Frage an!")

    # YouTube-Link
    if message.content.startswith('!youtube'):
        embedyoutube = discord.Embed(title='YouTube Kanal',
                                     description='Link zum YouTube Kanal',
                                     color=0xff0000)
        embedyoutube.add_field(name='Link', value='Link')
        embedyoutube.set_footer(text=Text')
        await message.channel.send(embed=embedyoutube)


    # Ban-System
    if message.content.startswith('!ban') and message.author.guild_permissions.ban_members:
        args = message.content.split(' ')
        if len(args) >= 2:
            banreason = ' '.join(args[2:])
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed7 = discord.Embed(title='Benutzer gebannt',
                                       description='Ein Benutzer wurde gebannt',
                                       color=0xff0000)
                embed7.add_field(name='Name des Benutzers', value='**{}**'.format(member.name))
                embed7.add_field(name='Grund', value='{}'.format(banreason))
                embed7.set_footer(text='Text')
                await message.channel.send(embed=embed7)

                embedbandm = discord.Embed(title='Du wurdest gebannt!',
                                           description='Du wurdest vom Discord gebannt!',
                                           color=0xff0000)
                embedbandm.add_field(name='Grund', value='{}'.format(banreason))
                embedbandm.set_footer(text='Text')

                try:
                    if not member.bot:
                        if not member.dm_channel:
                            await member.create_dm()
                        await member.dm_channel.send(embed=embedbandm)
                except discord.errors.Forbidden:
                    print('Es konnte keine Bannachricht an {0} gesendet werden.'.format(member.name))
                if member.bot:
                    print('Der User ist ein Bot.')
                await member.ban()

            else:
                await message.channel.send(f'Kein user mit dem Namen {args[1]} gefunden.')
        else:
            await message.channel.send('Bitte gib einen Namen an!')


    if message.content.startswith('!unban') and message.author.guild_permissions.ban_members:
        args = message.content.split(' ')
        unbanreason = ' '.join(args[2:])
        if len(args) >= 2:

            user: User = discord.utils.find(lambda m: args[1] in m.user.name, await message.guild.bans()).user
            if user:
                await message.guild.unban(user)
                embed8 = discord.Embed(title='Benutzer entbannt',
                                       description='Ein Benutzer wurde entbannt',
                                       color=0x04ff00)
                embed8.add_field(name='Name des Benutzers', value='**{}**'.format(user.name))
                embed8.add_field(name='Grund', value='{}'.format(unbanreason))
                embed8.set_footer(text='Game-Forum Discord Bot')
                await message.channel.send(embed=embed8)

                embedunbandm = discord.Embed(title='Du wurdest entbannt!',
                                             description='Du wurdest vom Discord entbannt!',
                                             color=0x04ff00)
                embedunbandm.add_field(name='Grund', value='{}'.format(unbanreason))
                embedunbandm.set_footer(text='Du kannst dem Discord nun wieder beitreten!')

                try:
                    if not user.bot:
                        if not user.dm_channel:
                            await user.create_dm()
                        await user.dm_channel.send(embed=embedunbandm)
                except discord.errors.Forbidden:
                    print('Es konnte keine Unbannachricht an {0} gesendet werden.'.format(member.name))
                if user.bot:
                    print('Der User ist ein Bot.')
            else:
                await message.channel.send(f'Kein user mit dem Namen {args[1]} gefunden.')
        else:
            await message.channel.send('Bitte gib einen Namen an!')

    #News-Command
    if message.content.startswith('!news') and message.author.permissions_in(message.channel).send_tts_messages:
        args = message.content.split(' ')
        if len(args) >= 3:
            titel = '{}'.format(args[1])
            news = ' ' .join(args[2:])
            embednews = discord.Embed(title='Eine neue News ist erschienen!',
                                    description='',
                                    color=0x04ff00)
            embednews.add_field(name='{}'.format(titel), value='{}'.format(news),
                                inline=False)
            embednews.set_footer(text="Text")
            await message.channel.purge(limit=1, check=is_not_pinned)
            await message.channel.send(embed = embednews)

    if message.content.startswith('!kick') and message.author.guild_permissions.kick_members:
        args = message.content.split(' ')
        kickreason = ' '.join(args[2:])
        if len(args) >= 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed9 = discord.Embed(title='Benutzer gekickt',
                                       description='Ein Benutzer wurde gekickt',
                                       color=0xfffb00)
                embed9.add_field(name='Name des Benutzers', value='**{}**'.format(member.name))
                embed9.add_field(name='Grund', value='{}'.format(kickreason))
                embed9.set_footer(text='Game-Forum Discord Bot')

                embedkickdm = discord.Embed(title='Du wurdest gekickt!',
                                            description='Du wurdest vom Discord gekickt!',
                                            color=0xfffb00)
                embedkickdm.add_field(name='Name des Benutzers', value='**{}**'.format(member.name))
                embedkickdm.add_field(name='Grund', value='{}'.format(kickreason))
                embedkickdm.set_footer(text='Du kannst dem Discord weiterhin beitreten!')
                await message.channel.send(embed=embed9)

                try:
                    if not member.bot:
                        if not member.dm_channel:
                            await member.create_dm()
                        await member.dm_channel.send(embed=embedkickdm)

                except discord.errors.Forbidden:
                    print('Es konnte keine Kicknachricht an {0} gesendet werden.'.format(member.name))

                if member.bot:
                    print('Der user ist ein Bot.')
                await member.kick()
            else:
                await message.channel.send(f'Kein User mit dem Namen {args[1]} gefunden.')
        else:
            await message.channel.send('Bitte gib einen Namen an!')

    if message.content.startswith('!warn') and message.author.guild_permissions.manage_nicknames:
        args = message.content.split(' ')
        warnreason = ' '.join(args[2:])
        if len(args) >= 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embedwarn = discord.Embed(title='Benutzer verwarnt',
                                          description='Ein Benutzer wurde verwarnt',
                                          color=0xfffb00)
                embedwarn.add_field(name='Name des Benutzers', value='**{}**'.format(member.name))
                embedwarn.add_field(name='Grund', value='{}'.format(warnreason))
                embedwarn.set_footer(text='Game-Forum Discord Bot')

                embedwarndm = discord.Embed(title='Du wurdest verwarnt',
                                            description='Du wurdest am Discord verwarnt!',
                                            color=0xfffb00)
                embedwarndm.add_field(name='Name des Benutzers', value='**{}**'.format(member.name))
                embedwarndm.add_field(name='Grund', value='{}'.format(warnreason))
                embedwarndm.set_footer(text='Du kannst dem Discord weiterhin beitreten!')
                await message.channel.send(embed=embedwarn)

                try:
                    if not member.bot:
                        if not member.dm_channel:
                            await member.create_dm()
                        await member.dm_channel.send(embed=embedwarndm)

                except discord.errors.Forbidden:
                    print('Es konnte keine Warnnachricht an {0} gesendet werden.'.format(member.name))
                if member.bot:
                    print('Der User ist ein Bot.')
            else:
                await message.channel.send(f'Kein user mit dem Namen {args[1]} gefunden.')
        else:
            await message.channel.send('Bitte gib einen Namen an!')

@client.event  # Beitritt des Servers
async def on_member_join(member):  # Willkommennachricht und Rollenvergabe für User
        mitgliedrolle = discord.utils.get(member.guild.roles, name='User')
        botrolle = discord.utils.get(member.guild.roles, name='BOT')
        willkommenschannel_id = # Channel ID
        willkommenschannel = client.get_channel(willkommenschannel_id)
        await willkommenschannel.send('Hey **{}**, willkommen auf dem Server!'.format(member.mention))
        embed = discord.Embed(title='Willkommen {} auf dem Game-Forun.net Discord Server! 👍 😀'.format(member.name),
                               description='Wir heißen dich herzlich Willkommen',
                               color=0x04ff00)
        embed.set_thumbnail(url=member.avatar_url)
        await willkommenschannel.send(embed=embed)

        if not member.bot:
            await member.add_roles(mitgliedrolle)
            embed = discord.Embed(title='Hey **{}**, willkommen auf dem Discord Server!'.format(member.name), description='Wir heißen dich herzlich willkommen und wünsche dir eine angenehme Zeit auf dem Server.', color=0x04ff00)
            try:
                if not member.dm_channel:
                    await member.create_dm()
                await member.dm_channel.send(embed=embed)
            except discord.errors.Forbidden:
                print('Ich konnte keine persönliche Willkommennachricht an **{}** senden'.format(member.name))

        if member.bot:
            await member.add_roles(botrolle)

client.run('Bot Token')