import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(name="setup", description="Set up the Crack an Egg server")
async def setup(interaction: discord.Interaction):

    # Only the server owner can use /setup
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used in a server.",
            ephemeral=True
        )
        return

    if interaction.guild.owner_id != interaction.user.id:
        await interaction.response.send_message(
            "❌ Only the server owner can use this command.",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)

    guild = interaction.guild

    # =========================
    # ROLES
    # =========================

    roles = [
        ("Owner", discord.Colour.red()),
        ("Admin", discord.Colour.orange()),
        ("Mod", discord.Colour.blue()),
        ("Member", discord.Colour.green())
    ]

    for role_name, colour in roles:
        existing_role = discord.utils.get(
            guild.roles,
            name=role_name
        )

        if existing_role is None:
            await guild.create_role(
                name=role_name,
                colour=colour,
                reason="Crack an Egg server setup"
            )

    # =========================
    # CATEGORIES + CHANNELS
    # =========================

    categories = {

        "📢 INFORMATION": [
            "👋・welcome",
            "📜・rules",
            "📢・announcements",
            "📰・updates",
            "🎁・codes"
        ],

        "💬 COMMUNITY": [
            "💬・general",
            "💡・suggestions",
            "🐛・bug-reports",
            "📸・media",
            "🎮・game-chat",
            "🔊・VC"
        ],

        "🛡️ STAFF": [
            "📋・staff-chat",
            "🚨・reports",
            "📑・mod-logs"
        ]
    }

    # =========================
    # CREATE EVERYTHING
    # =========================

    for category_name, channel_list in categories.items():

        # Find category if it already exists
        category = discord.utils.get(
            guild.categories,
            name=category_name
        )

        # Otherwise create it
        if category is None:
            category = await guild.create_category(
                category_name,
                reason="Crack an Egg server setup"
            )

        # Create channels
        for channel_name in channel_list:

            existing_channel = discord.utils.get(
                guild.channels,
                name=channel_name
            )

            if existing_channel is not None:
                continue

            # Voice channel
            if channel_name == "🔊・VC":

                await guild.create_voice_channel(
                    channel_name,
                    category=category,
                    reason="Crack an Egg server setup"
                )

            # Text channel
            else:

                await guild.create_text_channel(
                    channel_name,
                    category=category,
                    reason="Crack an Egg server setup"
                )

    await interaction.followup.send(
        "🥚 **Crack an Egg setup complete!**\n\n"
        "Created:\n"
        "👑 Owner\n"
        "🛡️ Admin\n"
        "🔨 Mod\n"
        "👤 Member\n\n"
        "📁 3 categories\n"
        "💬 All channels\n\n"
        "⚙️ Permissions were NOT changed.",
        ephemeral=True
    )


# =========================
# BOT READY
# =========================

@bot.event
async def on_ready():

    try:

        synced = await bot.tree.sync()

        print(f"Logged in as {bot.user}")
        print(f"Synced {len(synced)} slash command(s)")

    except Exception as error:

        print(f"Command sync error: {error}")


# =========================
# START BOT
# =========================

if not TOKEN:

    print("❌ ERROR: DISCORD_TOKEN is not set.")

else:

    bot.run(TOKEN)