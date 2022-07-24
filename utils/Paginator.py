import asyncio
import discord

from discord_components import Button, Interaction


class Paginator:

    def __init__(self, ctx, components_manager, pages: list = None, delete_after: int = None, timeout: int = 60):
        self.components_manager = components_manager
        self.delete_after = delete_after
        self.timeout = timeout
        self.pages = pages
        self.components_manager = components_manager
        self.current_page = 0
        self.ctx = ctx
        self.components = self.__setup_components()

    async def send(self):
        message = await self.ctx.send(
            embed=self.__get_embed(self.ctx.message.author),
            components=[
                [
                    self.components["previous"],
                    self.components["next"]
                ]
            ],
            delete_after=self.delete_after,
        )
        if self.delete_after is None:
            await asyncio.sleep(self.timeout)
            await message.edit(content="Timeout! Pagination will not be interactive.", components=[])

    def __get_embed(self, author: str):
        embed_data = self.pages[self.current_page]
        embed_data['footer'] = {
            'text': f"Requested by {author} | Page {self.current_page + 1}/{len(self.pages)}",
        }
        return discord.Embed.from_dict(embed_data)

    def __setup_components(self):
        components = {
            "next": Button(label="Next"),
            "previous": Button(label="Previous", disabled=True)
        }
        self.components_manager.add_callback(components["previous"], self.__previous)
        self.components_manager.add_callback(components["next"], self.__next)
        return components

    def __set_component_status(self):
        self.components["previous"].disabled = (self.current_page == 0)
        self.components["next"].disabled = (self.current_page == len(self.pages) - 1)

    async def __edit_embed(self, interaction: Interaction):
        await interaction.edit_origin(
            embed=self.__get_embed(interaction.user),
            components=[
                [
                    self.components["previous"],
                    self.components["next"]
                ]
            ]
        )

    async def __previous(self, interaction: Interaction):
        self.current_page -= 1
        self.__set_component_status()
        await self.__edit_embed(interaction)

    async def __next(self, interaction: Interaction):
        self.current_page += 1
        self.__set_component_status()
        await self.__edit_embed(interaction)
