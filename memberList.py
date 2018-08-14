#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# bot_bcad_3.6.py

import asyncio
import discord
import json
from discord.ext import commands

async def membersDump(ctx):
    with open('members.log', 'r', newline='\n', encoding='utf-8') as members_list_raw:
        members_list = members_list_raw.read()
        member = ctx.message.author
        await ctx.bot.send_message(member, members_list)

async def membersLog(ctx):
    for server in ctx.bot.servers:
        with open('members.log', 'w+', encoding='utf-8') as outfile:  
            for i,member in enumerate(server.members):
                list_mem_num = (f'{i}')
                list_mem_id = (f'{member.id}')
                list_mem = (f'{member}')
                list_mem_name = (f'{member.name}')
                list_all = (f'Number: {list_mem_num} ID: {list_mem_id} Name: {list_mem} ({list_mem_name})\n')
                with open('members.log', 'a') as file:
                    file.write(list_all)
                             
    await ctx.bot.say('List saved into logs.')

