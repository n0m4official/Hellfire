import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from .anime_api import AnimeAPI

# This file causes me so much pain -_-
# Spent hours debugging issues with fields being None and crashing the bot
# Also had to implement pagination for search results, which took way longer than expected
# Nextcord's UI system is powerful but can be complex to work with correctly
# Kudos to their devs for making it possible, but damn it was a headache to get right

# Pagination View for multiple results
# Allows users to navigate through multiple embeds using buttons
# Handles timeouts and disables buttons after inactivity

class PagedView(nextcord.ui.View):
    def __init__(self, pages, timeout=120):
        super().__init__(timeout=timeout)
        self.pages = pages
        self.index = 0

    async def update_message(self, interaction):
        embed = self.pages[self.index]
        await interaction.response.edit_message(embed=embed, view=self)

    @nextcord.ui.button(label="⬅️ Previous", style=nextcord.ButtonStyle.grey)
    async def previous(self, button, interaction: nextcord.Interaction):
        if self.index > 0:
            self.index -= 1
        await self.update_message(interaction)

    @nextcord.ui.button(label="Next ➡️", style=nextcord.ButtonStyle.grey)
    async def next(self, button, interaction: nextcord.Interaction):
        if self.index < len(self.pages) - 1:
            self.index += 1
        await self.update_message(interaction)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

class AnimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = AnimeAPI()

    # Without this, fields with None values cause the bot to crash
    # I spent far too long debugging this issue -_-
    # This thing, made me want to punch my monitor...
    def safe(self, value):
      return value if value not in (None, "") else "Unknown"

    def cog_unload(self):
        self.bot.loop.create_task(self.api.close())

    # ----------------------------
    # Helper to trim descriptions
    # ----------------------------
    def trim(self, text):
        if not text:
            return "No description available."
        clean = text.replace("<br>", "").replace("<i>", "").replace("</i>", "")
        return clean[:500] + "..." if len(clean) > 500 else clean

    # ----------------------------
    # /anime search
    # ----------------------------
    @nextcord.slash_command(name="anime", description="Search for an anime (title or genre)")
    async def anime(self, interaction: nextcord.Interaction,
                    query: str = SlashOption(description="Anime title or genre")):

        await interaction.response.defer()

        # Known AniList genres for anime
        GENRES = {
            "action", "adventure", "comedy", "drama", "ecchi", "fantasy",
            "hentai", "horror", "mahou shoujo", "mecha", "music", "mystery",
            "psychological", "romance", "sci-fi", "slice of life",
            "sports", "supernatural", "thriller", "isekai"
        }

        user_query = query.lower()

        # -----------------------------------
        # 1. GENRE SEARCH
        # -----------------------------------
        if user_query in GENRES:
            data = await self.api.anilist_anime_by_genre(query)
            media = data["data"]["Page"]["media"]

            if not media:
                return await interaction.followup.send(f"No anime found under genre **{query}**.")

            m = media[0]  # take first match

        else:
            # -----------------------------------
            # 2. TITLE SEARCH
            # -----------------------------------
            data = await self.api.anilist_search(query)
            media = data["data"]["Page"]["media"]

            if not media:
                return await interaction.followup.send("No results found.")

            m = media[0]

        # -----------------------------------
        # Build Embed
        # -----------------------------------
        embed = nextcord.Embed(
            title=m["title"]["english"] or m["title"]["romaji"],
            description=self.trim(m["description"]),
            color=0x00B2FF
        )

        embed.set_thumbnail(url=m["coverImage"]["large"])
        embed.add_field(name="Episodes", value=self.safe(m["episodes"]))
        embed.add_field(name="Score", value=self.safe(m["averageScore"]))
        embed.add_field(name="Genres", value=", ".join(m["genres"]))
        embed.add_field(name="AniList URL", value=m["siteUrl"])

        pages = []

        # Build 1-page or multi-page result
        for m in media[:10]:  # top 10 max
            embed = nextcord.Embed(
                title=m["title"]["english"] or m["title"]["romaji"],
                description=self.trim(m["description"]),
                color=0x00B2FF
            )
            embed.set_thumbnail(url=m["coverImage"]["large"])
            embed.add_field(name="Episodes", value=self.safe(m["episodes"]))
            embed.add_field(name="Score", value=self.safe(m["averageScore"]))
            embed.add_field(name="Genres", value=", ".join(m["genres"]))
            embed.add_field(name="AniList URL", value=m["siteUrl"])
            pages.append(embed)

        view = PagedView(pages)
        await interaction.followup.send(embed=pages[0], view=view)


    # ----------------------------
    # /manga search
    # ----------------------------
    @nextcord.slash_command(name="manga", description="Search for a manga (title or genre)")
    async def manga(self, interaction: nextcord.Interaction,
                    query: str = SlashOption(description="Manga title or genre")):

        await interaction.response.defer()

        # Known AniList genres for manga
        GENRES = {
            "action", "adventure", "comedy", "drama", "ecchi", "fantasy",
            "hentai", "horror", "mahou shoujo", "mecha", "music", "mystery",
            "psychological", "romance", "sci-fi", "slice of life",
            "sports", "supernatural", "thriller", "isekai"
        }

        user_query = query.lower()

        # -----------------------------------
        # 1. GENRE SEARCH
        # -----------------------------------
        if user_query in GENRES:
            data = await self.api.anilist_manga_by_genre(query)
            media = data["data"]["Page"]["media"]

            if not media:
                return await interaction.followup.send(f"No manga found under genre **{query}**.")

            m = media[0]  # Take first top match

        else:
            # -----------------------------------
            # 2. TITLE SEARCH
            # -----------------------------------
            data = await self.api.anilist_manga(query)
            media = data["data"]["Page"]["media"]

            if not media:
                return await interaction.followup.send("No results found.")

            m = media[0]

        # -----------------------------------
        # Build Embed
        # -----------------------------------
        embed = nextcord.Embed(
            title=m["title"]["english"] or m["title"]["romaji"],
            description=self.trim(m["description"]),
            color=0xFFC300
        )

        embed.set_thumbnail(url=m["coverImage"]["large"])
        embed.add_field(name="Chapters", value=self.safe(m["chapters"]))
        embed.add_field(name="Volumes", value=self.safe(m["volumes"]))
        embed.add_field(name="Score", value=self.safe(m["averageScore"]))
        embed.add_field(name="Genres", value=", ".join(m["genres"]))
        embed.add_field(name="AniList URL", value=m["siteUrl"])

        pages = []

        for m in media[:10]:
            embed = nextcord.Embed(
                title=m["title"]["english"] or m["title"]["romaji"],
                description=self.trim(m["description"]),
                color=0xFFC300
            )
            embed.set_thumbnail(url=m["coverImage"]["large"])
            embed.add_field(name="Chapters", value=self.safe(m["chapters"]))
            embed.add_field(name="Volumes", value=self.safe(m["volumes"]))
            embed.add_field(name="Score", value=self.safe(m["averageScore"]))
            embed.add_field(name="Genres", value=", ".join(m["genres"]))
            embed.add_field(name="AniList URL", value=m["siteUrl"])
            pages.append(embed)

        view = PagedView(pages)
        await interaction.followup.send(embed=pages[0], view=view)


    # ----------------------------
    # /character search
    # ----------------------------
    @nextcord.slash_command(name="character", description="Search anime characters")
    async def character(self, interaction: nextcord.Interaction,
                        query: str = SlashOption(description="Character name")):

        await interaction.response.defer()

        data = await self.api.anilist_character(query)
        chars = data["data"]["Page"]["characters"]

        if not chars:
            return await interaction.followup.send("No characters found.")

        c = chars[0]

        embed = nextcord.Embed(
            title=c["name"]["full"],
            description=self.trim(c["description"]),
            color=0xFF66CC
        )
        embed.set_thumbnail(url=c["image"]["large"])
        embed.add_field(name="Native", value=c["name"]["native"])
        embed.add_field(name="AniList URL", value=c["siteUrl"])

        await interaction.followup.send(embed=embed)

    # ----------------------------
    # /trending – Jikan top anime
    # ----------------------------
    @nextcord.slash_command(name="trending", description="Show trending anime")
    async def trending(self, interaction: nextcord.Interaction):

        await interaction.response.defer()

        data = await self.api.jikan_top()
        top = data["data"][:10]

        embed = nextcord.Embed(
            title="🔥 Trending Anime (MAL)",
            description="Top 10 trending anime right now.",
            color=0xFF4500
        )

        for i, item in enumerate(top, start=1):
            embed.add_field(
                name=f"{i}. {item['title']}",
                value=f"Score: {item['score']}\nEpisodes: {item['episodes']}",
                inline=False
            )

        await interaction.followup.send(embed=embed)

def setup(bot):
    bot.add_cog(AnimeCog(bot))
