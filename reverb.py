import os
import re
import discord
import asyncio
import gspread
from datetime import datetime
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Discord bot setup
intents = discord.Intents.all()
intents.members = True  # to enable member related events
bot = commands.Bot(command_prefix='/', intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

# Google Spreadsheet API setup
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('harmonizer.json', scope)
client_gspread = gspread.authorize(creds)


spreadsheet_id = '1WSrmJKpEU8uC0UIFiS5n2Yx6O4BspaJfCaEEeUV_a2A'

# Specify the name of the sheet you want to access
payment = 'Payment Information'
tier_ph = 'PH - Content'
tier_id = 'ID - Content'
tier_th = 'TH - Content'
badge = 'Tier Ranking'

# Open the sheet by spreadsheet id and sheet name
payment_sheet = client_gspread.open_by_key(spreadsheet_id).worksheet(payment)
tierPH = client_gspread.open_by_key(spreadsheet_id).worksheet(tier_ph)
tierID = client_gspread.open_by_key(spreadsheet_id).worksheet(tier_id)
tierTH = client_gspread.open_by_key(spreadsheet_id).worksheet(tier_th)
badge = client_gspread.open_by_key(spreadsheet_id).worksheet(badge)

@bot.command()
async def PaymentInformation(ctx):
        timeout_message = "Uh-oh! It's been 10 minutes since we last talked! Don't leave me hanging, friend! Just type **/hello** and we can get back to chatting. Meet me over at the Harmonizer bot in the Reverb Club Discord Server. Can't wait to hear from you again!"
        now = datetime.now()
        header = ['Time and Date of Submission','Name', 'Content Link', 'Analytics', 'Nationality', 'Instagram', 'Tiktok', 'Bank', 'Bank Account Name', 'Bank Account Number', 'Email', 'Contact Number']
        
        # Create a dictionary to hold the user inputs
        user_inputs = {category: '' for category in header}

        try:
            #1
            await ctx.author.send("Please respond with a link to your content.")
            while True:
                try:
                    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
                    user_input = response.content.strip()
                    if re.match(r"^https?:\/\/www\.\w+\.\w+\/?.*$", user_input):
                        user_inputs['Content Link'] = response.content
                        break
                    await ctx.author.send("Invalid input. Please reply with a website URL in the 'https://www.website.com/' format.")
                except asyncio.TimeoutError:
                    await ctx.author.send(timeout_message)
                    return
                
            user_inputs['Content Link'] = response.content
            
            #2
            await ctx.author.send("Next, please upload the analytics screenshots of your content. Please ensure that the following are visible in your screenshot: Views, Impressions, and Engagements")

            screenshots = []

            while True:
                try:
                    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
                    if len(response.attachments) > 0:
                        for attachment in response.attachments:
                            screenshots.append(attachment.url)
                    elif response.content:
                        await ctx.author.send("Invalid input. Please upload the analytics screenshots of your content.")
                        continue
                    if len(screenshots) == len(response.attachments):
                        break
                except asyncio.TimeoutError:
                    await ctx.author.send(timeout_message)
                    break

            if screenshots:
                screenshot_links = '\n'.join(screenshots)
                user_inputs['Analytics'] = screenshot_links

                


            
            #3
            await ctx.author.send("Thanks! Kindly reply \"PH\" if you're from the Philippines, \"ID\" if you're from Indonesia, and \"TH\" if you're from Thailand.")
            while True:
                try:
                    #response = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=None)
                    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
                    user_input = response.content.upper()
                    if user_input in ["PH", "ID", "TH"]:
                        user_inputs['Nationality'] = user_input
                        break
                    else:
                        await ctx.author.send("Invalid input. Please reply with \"PH\" for Philippines, \"ID\" for Indonesia, or \"TH\" for Thailand.")
                except asyncio.TimeoutError:
                    await ctx.author.send(timeout_message)
                    return

            #4
            await ctx.author.send("Please reply with your name.")
            #response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
            user_inputs['Name'] = response.content
                
            #5
            await ctx.author.send("Next, what's your Instagram Handle? If not applicable, please respond with NA")
            #response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
            user_inputs['Instagram'] = response.content

            #6
            await ctx.author.send("Next, what's your TikTok Handle? If not applicable, please respond with NA")
            #response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
            user_inputs['Tiktok'] = response.content

            #7
            await ctx.author.send("Next, what's your Bank Name? Please double check before sending.")
            #response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
            user_inputs['Bank'] = response.content

            #8
            await ctx.author.send("Next, what's your Bank Account Name? Please double check before sending. We will not be liable if your payment goes to the wrong recipient due to incorrect information.")
            #response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
            user_inputs['Bank Account Name'] = response.content

            #9
            await ctx.author.send("Next, what's your Bank Account Number? Please double check before sending. We will not be liable if your payment goes to the wrong recipient due to incorrect information.")
            while True:
                try:
                    #response = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=None)
                    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
                    user_input = response.content.strip()
                    if user_input.isdigit():
                        user_inputs['Bank Account Number'] = user_input
                        break
                    else:
                        await ctx.author.send("Invalid input. Please reply with numerical data only.")
                except asyncio.TimeoutError:
                    await ctx.author.send(timeout_message)
                    return

            #10
            await ctx.author.send("Next, please reply with your email address.")
            while True:
                try:
                    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
                    user_input = response.content.strip()
                    if re.match(r"[^@]+@[^@]+\.[^@]+", user_input):
                        user_inputs['Email'] = user_input
                        break
                    await ctx.author.send("Invalid input. Please reply with an email in the 'name@website.com' format.")
                except asyncio.TimeoutError:
                    await ctx.author.send(timeout_message)
                    return

            #11
            await ctx.author.send("Lastly, please reply with your contact number.")
            while True:
                try:
                    #response = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=None)
                    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
                    user_input = response.content.strip()
                    if user_input.isdigit():
                        user_inputs['Contact Number'] = user_input
                        break
                    else:
                        await ctx.author.send("Invalid input. Please reply with numerical data only.")
                except asyncio.TimeoutError:
                    await ctx.author.send(timeout_message)
                    return

            await ctx.author.send("Thanks for providing these information. Rest assured that your information is safe with us. Please wait for further updates from your coordinator through the Reverb Discord Channel. Thank you!")
            
            user_inputs['Time and Date of Submission'] = now.strftime("%m/%d/%Y %H:%M:%S")
            
            payment_sheet.append_row([user_inputs[category] for category in header])

        except discord.Forbidden:
            await ctx.send("It appears that I do not have permission to send you messages. To enable us to chat, please follow these steps at https://www.getdroidtips.com/direct-messages-discord/ to adjust your settings accordingly.")
        except asyncio.TimeoutError:
            await ctx.author.send(timeout_message)
        except Exception as e:
            print(e)
            
                
@bot.command()
async def hello(ctx):

    intro_message = """Hey there! I'm Harmonizer, your friendly neighborhood Discord bot from Reverb Club! I'm here to make your content creation journey a breeze and add some fun to the mix!

Ready to get started? Just send me a quick command and I'll do the rest! Send **/CheckContent** to get your content reviewed and approved, **/PaymentInformation** to submit your payment info and get paid like a pro, or **/TierRanking** to find out if you're Gold, Silver, or Bronze superstar!

Let's make some magic together! Where would you like to begin?"""
    await ctx.send(intro_message)
    
@bot.command()
async def TierRanking(ctx):
    timeout_message = "Uh-oh! It's been 10 minutes since we last talked! Don't leave me hanging, friend! Just type **/hello** and we can get back to chatting. Meet me over at the Harmonizer bot in the Reverb Club Discord Server. Can't wait to hear from you again!"
    try:
        
        
        await ctx.author.send("Now, please give me your username and let's see what tier you're at.")
        response = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
        fullname = response.content
        badge_records = badge.get_all_records()
        
        try:
            badge_records = badge.get_all_records()
            user_record = None
            user_record = next(record for record in badge_records if record['Content Creator'].lower() == fullname.lower())
        except StopIteration:
            return await ctx.author.send(f"Aw, snap! I couldn't find your username! You must be a rare gem in the Reverb Discord Server! Can you give me one more shot by sending another /TierRanking command? Let's see if I can uncover your tier this time! 😎")
        
        # Create an embed with the user's information and send it to the user
        value = user_record['Lyrics Q1 2023']
        tier_emoji = {'Gold': '🥇', 'Silver': '🥈', 'Bronze': '🥉'}.get(value, '')
        embed = discord.Embed(title=f"{fullname}'s Tier")
        embed.add_field(name="Tier Ranking", value=value + tier_emoji)

        message = f"You're doing amazing, {fullname}! You're currently in the {value} tier."
        if value == 'Gold':
            message += ' Congratulations! 🎊'
        else:
            message += ' Keep it up and aim for the Gold!🥇'

        await ctx.author.send(message)
        await ctx.author.send(embed=embed)
        await ctx.author.send("If you need any help, just say /hello in the Reverb Discord Server and I'll be here for you!")
    
    except discord.Forbidden:
        await ctx.send("It appears that I do not have permission to send you messages. To enable us to chat, please follow these steps at https://www.getdroidtips.com/direct-messages-discord/ to adjust your settings accordingly.")
    except asyncio.TimeoutError:
        await ctx.author.send(timeout_message)
    except Exception as e:
        print(e)
        
        
@bot.command()
async def CheckContent(ctx):
    timeout_message = "Uh-oh! It's been 10 minutes since we last talked! Don't leave me hanging, friend! Just type **/hello** and we can get back to chatting. Meet me over at the Harmonizer bot in the Reverb Club Discord Server. Can't wait to hear from you again!"
    
    now2 = datetime.now()
    header2 = ['Time and Date of Submission', 'User Name', 'Caption']
    user_inputs2 = {category: '' for category in header2}
    
    try:
        message = (
            "Hello! This is Reverb Club's Discord bot for reviewing and approval "
            "of text-based content for your assigned campaigns.\n\nKindly reply "
            "\"PH\" if you're from the Philippines, \"ID\" if you're from "
            "Indonesia, and \"TH\" if you're from Thailand."
        )
        await ctx.author.send(message)

        while True:
            
            response2 = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
            country = response2.content.upper()

            if country in ['PH', 'ID', 'TH']:
                break
            else:
                await ctx.author.send("Invalid input. Please reply with \"PH\" for Philippines, \"ID\" for Indonesia, or \"TH\" for Thailand.")

        await ctx.author.send("What is your username?")
        response2 = await bot.wait_for('message', check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=600)
        user_inputs2['User Name'] = response2.content
        
        required_tags = (
            """For LyricsQ1, please make sure that you have followed these: 

            - Required hashtags: 1) **#WorkingWithSpotify**, 2) **#ParinigMoWithSpotify**
            - Required tags: **@spotifyph**
            - Use only standard keyboard emojis and images/graphics that you own
            - Be natural and authentic! Your captions shouldn't sound like an ad :)
            ⠀⠀⠀⠀⠀⠀⠀
            """
        )
        await ctx.author.send(required_tags)

        while True:
            message = "Please reply with **Yes** if you understand the instructions above."
            await ctx.author.send(message)

            response2 = await bot.wait_for(
                'message',
                check=lambda message: (
                    message.author == ctx.author and 
                    isinstance(message.channel, discord.DMChannel)
                ), 
                timeout=600
            )
            agree = response2.content.upper()

            if agree == 'YES':
                break
            else:
                return await CheckContent(ctx)

        message = "Hooray! Please share your caption in the box below."
        await ctx.author.send(message)

        response2 = await bot.wait_for(
            'message', 
            check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), 
            timeout=600
        )
        caption = response2.content

        while True:
            if "#WorkingWithSpotify" not in caption or "#ParinigMoWithSpotify" not in caption or "@spotifyph" not in caption:
                message = "Oops, looks like you missed some of the guidelines. Please check and try again!"
                await ctx.author.send(message)
                await ctx.author.send("Here are the guidelines again:\n\n- Use #WorkingWithSpotify and #ParinigMoWithSpotify hashtags\n- Tag @spotifyph\n- Keep it real! No ad-like captions, please.\n\nGot it? Reply with **Yes**")
                response2 = await bot.wait_for(
                    'message', 
                    check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), 
                    timeout=600
                )
                if response2.content.lower() == 'yes':
                    await ctx.author.send("You're crushing it! Please revise your caption with the required tags and submit it below. ")
                    new_content = await bot.wait_for(
                    'message', 
                    check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), 
                    timeout=600
                )
                    caption = new_content.content
                else:
                    ""
            else:
                break
            
        user_inputs2['Caption'] = caption
        await ctx.author.send("Congratulations! Your content has passed the first round of review. Please wait for further instructions through the Reverb Discord channel.")

        user_inputs2['Time and Date of Submission'] = now2.strftime("%m/%d/%Y %H:%M:%S")

        if country == 'PH':
            tierPH.append_row([user_inputs2[category] for category in header2])
        elif country == 'TH':
            tierTH.append_row([user_inputs2[category] for category in header2])
        elif country == 'ID':
            tierID.append_row([user_inputs2[category] for category in header2])
    
    except discord.Forbidden:
        await ctx.send("It appears that I do not have permission to send you messages. To enable us to chat, please follow these steps at https://www.getdroidtips.com/direct-messages-discord/ to adjust your settings accordingly.")
    except asyncio.TimeoutError:
        await ctx.author.send(timeout_message)
    except Exception as e:
        print(e)
    
bot.run(TOKEN)