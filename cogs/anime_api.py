import aiohttp

# This class handles all interactions with external anime/manga APIs
# Currently supports AniList, Jikan (MyAnimeList), and MangaDex
# Does not store any user data
# API documentation:
# AniList: https://anilist.github.io/ApiV2-GraphQL-Docs
# Jikan: https://docs.api.jikan.moe/
# MangaDex: https://api.mangadex.org/docs/v2/

# Note: Rate limiting is not handled here; users of this class should implement their own rate limiting if necessary
# This class uses aiohttp for asynchronous HTTP requests
# Ensure to close the aiohttp session when done using the close() method
# Example usage:
# api = AnimeAPI()

# This file was created to modularize API interactions for better maintainability and readability
# And caused me so much pain to implement correctly... I spent way too long debugging issues with aiohttp requests, JSON parsing, and GraphQL queries
# The worst part was that some of the issues only manifested under certain conditions, making them hard to track down
# FOR SOME REASON THE APIS WOULD JUST STOP RESPONDING AT RANDOM TIMES??? LIKE WHAT THE HELL???
# sidenotes: 
#           WHY DO THE APIS USE DIFFERENT FORMATS??? LIKE ANI LIST USES GRAPHQL WHILE JIKAN AND MANGADEX USE REST????
#           WHY DO THE APIS NOT RECOGNIZE TAGS VS GENRES CONSISTENTLY??? LIKE ANI LIST USES TAGS BUT MANGADEX USES GENRES???
#           WHY DO I HAVE TO SPEND 10 HOURS JUST TO GET A BASIC IMPLEMENTATION OF THIS???


class AnimeAPI:
    BASE_ANILIST = "https://graphql.anilist.co"
    BASE_JIKAN = "https://api.jikan.moe/v4"
    BASE_MANGADEX = "https://api.mangadex.org"

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def close(self):
        await self.session.close()

    # -----------------------------
    # AniList — Anime Title Search
    # -----------------------------
    async def anilist_search(self, query):
        gql_query = """
        query ($query: String) {
            Page {
                media(search: $query, type: ANIME) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    description
                    episodes
                    coverImage {
                        large
                    }
                    averageScore
                    genres
                    siteUrl
                }
            }
        }
        """

        variables = {"query": query}

        async with self.session.post(
            self.BASE_ANILIST, json={"query": gql_query, "variables": variables}
        ) as resp:
            return await resp.json()

    # -----------------------------
    # AniList — Manga Title Search
    # -----------------------------
    async def anilist_manga(self, query):
        gql_query = """
        query ($query: String) {
            Page {
                media(search: $query, type: MANGA) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    description
                    chapters
                    volumes
                    coverImage {
                        large
                    }
                    averageScore
                    genres
                    siteUrl
                }
            }
        }
        """

        variables = {"query": query}

        async with self.session.post(
            self.BASE_ANILIST, json={"query": gql_query, "variables": variables}
        ) as resp:
            return await resp.json()

    # -----------------------------
    # AniList — Character Search
    # -----------------------------
    async def anilist_character(self, query):
        gql_query = """
        query ($query: String) {
            Page {
                characters(search: $query) {
                    id
                    name {
                        full
                        native
                    }
                    image {
                        large
                    }
                    description
                    siteUrl
                }
            }
        }
        """

        variables = {"query": query}

        async with self.session.post(
            self.BASE_ANILIST, json={"query": gql_query, "variables": variables}
        ) as resp:
            return await resp.json()

    # ---------------------------------------------------------
    # AniList — Manga Genre/Tag Search  (FIXED: uses tag_in)
    # ---------------------------------------------------------
    async def anilist_manga_by_genre(self, genre):
        gql_query = """
        query ($genre: String) {
            Page {
                media(tag_in: [$genre], type: MANGA) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    description
                    chapters
                    volumes
                    coverImage {
                        large
                    }
                    averageScore
                    genres
                    siteUrl
                }
            }
        }
        """

        variables = {"genre": genre}

        async with self.session.post(
            self.BASE_ANILIST, json={"query": gql_query, "variables": variables}
        ) as resp:
            return await resp.json()

    # ---------------------------------------------------------
    # AniList — Anime Genre/Tag Search  (FIXED: uses tag_in)
    # ---------------------------------------------------------
    async def anilist_anime_by_genre(self, genre):
        gql_query = """
        query ($genre: String) {
            Page {
                media(tag_in: [$genre], type: ANIME) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    description
                    episodes
                    coverImage {
                        large
                    }
                    averageScore
                    genres
                    siteUrl
                }
            }
        }
        """

        variables = {"genre": genre}

        async with self.session.post(
            self.BASE_ANILIST, json={"query": gql_query, "variables": variables}
        ) as resp:
            return await resp.json()

    # -----------------------------
    # Jikan — Trending Anime
    # -----------------------------
    async def jikan_top(self):
        async with self.session.get(f"{self.BASE_JIKAN}/top/anime") as resp:
            return await resp.json()

    # -----------------------------
    # MangaDex — Manga Search
    # -----------------------------
    async def mangadex_search(self, title):
        params = {"title": title, "limit": 5}
        async with self.session.get(f"{self.BASE_MANGADEX}/manga", params=params) as resp:
            return await resp.json()
