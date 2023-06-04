# HIMA Discord Bots and SQLite API

This repository contains the code for Discord bots and an API built for an NFT project. The bots are developed using the PyCord library, while the API is built with FastAPI and utilizes a SQLite database hosted on a VPS.

## Overview

The NFT Project Discord Bots and SQLite API showcase the implementation of Discord bots and an API designed for an NFT project. These components demonstrate the integration of PyCord, FastAPI, and SQLite to provide functionality related to the NFT project within the Discord platform.

## The project consists of three bots:

- Attendance Bot: This bot resets daily and requires users to participate in taking attendance. Users need to use a specific command each day to mark their attendance. The bot stores this information in the database and displays the number of consecutive attendance days for each user. It also provides a leaderboard showing the top users in the server.

- Points Bot: The Points Bot randomly sends messages to the chat at various intervals and asks users pre-written questions. The first user to reply correctly receives a point. Some users may have multipliers based on the number of NFTs they own, increasing their chances of earning points.

- Shop Bot: The Shop Bot allows users to spend their accumulated points. Users can purchase items such as a Medical Certificate, which patches up their attendance streak if they miss a day. Additionally, the bot offers roles used in NFT giveaways to reward users.
