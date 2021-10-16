# telegram weather chatbot

## What does it do?
[contact_link])(https://telegram.me/Sam_weatherreport_bot)

This repository is a telegram chatbot which gives you weather information to the specific region.
The weather information is crawled from Central Weather Bureau. In my opinion, it's a reliable source of weather information.
Currently, it supports region of 新竹市東區、台北市南港區、台北市信義區、基隆市中山區、新北市汐止區
The chatbot offers you with a interactive conversation which makes it easy for user to acquire the corresponding information.
Beside the text information, it also draws line graph for visual representatoin.
[example](https://i.imgur.com/F6bVtb0.png)

## How it work?
Fill in your own telegram API token in 'telegram_token' of conversation.py and 'auth' of weather_fun.py
Fill in your API token of Central Weather Bureau in 'auth_code' of weather_fun.py
Then, run conversation.py, it will collect the data from Central Weather Bureau and send it back to the user who requested it.