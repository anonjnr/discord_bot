#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# bot_bcad_3.6.py

import utilities

async def membersDump(ctx):
    with open('./logs/members.log', 'r', newline='\n', encoding='utf-8') as members_list_raw:
        members_list = members_list_raw.read()
        member = ctx.message.author
        await ctx.bot.send_message(member, members_list)


async def membersLog(ctx):
    log_path = ("./logs/members" + "-server-" + ctx.message.server.name + "-" + (utilities.epoch_to_custom_date(utilities.FMT_TIME_FILE)) + ".log")
    for i, member in enumerate(ctx.message.server.members):
        list_mem_num = (f'{i}')
        list_mem_id = (f'{member.id}')
        list_mem = (f'{member}')
        list_mem_name = (f'{member.name}')
        list_all = (f'Number: {list_mem_num} ID: {list_mem_id} Name: {list_mem} ({list_mem_name})\n')
        with open(log_path, 'a') as file:
            file.write(list_all)
    for channel in ctx.message.server.channels:
        if channel.name == 'logs':
            await ctx.bot.send_file(channel, log_path)
    await ctx.bot.send_file(ctx.message.author, log_path)
