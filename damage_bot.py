import discord
from discord.ext import commands
import asyncio
import matplotlib.pyplot as plt
import io
from dotenv import load_dotenv
load_dotenv()

import lol_api  # IMPORTANT: import module, not *

import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print("Damage bot online ✅")

@client.command()
async def helpme(ctx):
    help_message = (
        "**🎮 Arena Damage Bot — Commands**\n"
        "--------------------------------------\n\n"

        "**🔥 Damage Leaderboards**\n"
        "• `!damage [games]`\n"
        "  → Shows **average damage per game** (Arena only)\n"
        "  → Example: `!damage 10`\n\n"

        "• `!damage_total [games]`\n"
        "  → Shows **total damage** (Arena only)\n"
        "  → Example: `!damage_total 15`\n\n"

        "**📊 Visuals**\n"
        "• `!damage_graph [games]`\n"
        "  → Generates a **bar graph** of average Arena damage\n"
        "  → Example: `!damage_graph 10`\n\n"

        "**📋 Tables**\n"
        "• `!damage_table [games]`\n"
        "  → Displays a **text table** with avg & total damage\n"
        "  → Example: `!damage_table 8`\n\n"

        "**⚙️ Notes**\n"
        "• `[games]` is optional (default = 10)\n"
        "• Only **Arena games** are counted\n"
        "• Rankings are sorted from **highest → lowest**\n"
        "• Bot may take a few seconds to respond (Riot API)\n\n"

        "**💡 Examples**\n"
        "• `!damage`\n"
        "• `!damage 5`\n"
        "• `!damage_graph 12`\n"
    )

    await ctx.send(help_message)

# -----------------------------
# DAMAGE LEADERBOARD (AVG)
# -----------------------------
@client.command()
async def damage(ctx, games: int = 10):
    await ctx.send("🔍 Fetching Arena damage data...")

    try:
        results = await asyncio.to_thread(lol_api.fetch_damage_data, games)

        sorted_results = sorted(
            results.items(),
            key=lambda x: x[1]["avg"],
            reverse=True
        )

        lines = ["**🔥 Arena Damage Leaderboard (AVG)**"]

        for rank, (riot_id, stats) in enumerate(sorted_results, start=1):
            lines.append(
                f"**#{rank} {riot_id}** — "
                f"{stats['avg']:,.0f} avg dmg "
                f"({stats['games']} games)"
            )

        await ctx.send("\n".join(lines))

    except Exception as e:
        await ctx.send(f"❌ Error:\n```{e}```")


# -----------------------------
# DAMAGE LEADERBOARD (TOTAL)
# -----------------------------
@client.command()
async def damage_total(ctx, games: int = 10):
    await ctx.send("🔍 Fetching Arena damage data...")

    results = await asyncio.to_thread(lol_api.fetch_damage_data, games)

    sorted_results = sorted(
        results.items(),
        key=lambda x: x[1]["total"],
        reverse=True
    )

    lines = ["**🔥 Arena Damage Leaderboard (TOTAL)**"]

    for rank, (riot_id, stats) in enumerate(sorted_results, start=1):
        lines.append(
            f"**#{rank} {riot_id}** — "
            f"{stats['total']:,} total dmg "
            f"({stats['games']} games)"
        )

    await ctx.send("\n".join(lines))


# -----------------------------
# DAMAGE GRAPH
# -----------------------------
@client.command()
async def damage_graph(ctx, games: int = 10):
    await ctx.send("📊 Generating damage graph...")

    results = await asyncio.to_thread(lol_api.fetch_damage_data, games)

    names = []
    averages = []

    for riot_id, stats in sorted(
        results.items(),
        key=lambda x: x[1]["avg"],
        reverse=True
    ):
        names.append(riot_id)
        averages.append(stats["avg"])

    plt.figure(figsize=(8, 5))
    plt.bar(names, averages)
    plt.ylabel("Average Damage")
    plt.title("Arena Average Damage")
    plt.xticks(rotation=30, ha="right")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close()

    file = discord.File(buf, filename="arena_damage.png")
    await ctx.send(file=file)


# -----------------------------
# DAMAGE TABLE
# -----------------------------
@client.command()
async def damage_table(ctx, games: int = 10):
    results = await asyncio.to_thread(lol_api.fetch_damage_data, games)

    sorted_results = sorted(
        results.items(),
        key=lambda x: x[1]["avg"],
        reverse=True
    )

    table = ["Rank | Player | Games | Avg Dmg | Total Dmg"]
    table.append("-" * 45)

    for rank, (riot_id, stats) in enumerate(sorted_results, start=1):
        table.append(
            f"{rank:>4} | {riot_id:<18} | "
            f"{stats['games']:>5} | "
            f"{stats['avg']:>7.0f} | "
            f"{stats['total']:>9}"
        )

    await ctx.send(f"```{chr(10).join(table)}```")


client.run(TOKEN)
