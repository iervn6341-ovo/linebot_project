from linebot import LineBotApi
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('XI7nR5ztvkRzKMIGcbBbm5zxL7xj1uf4tTS5TrgltV93aCV1uCby0eUr0S0NHbgFNDMXIjK/E7vqqfAnjfYnDUbobs9e4WN4A+uSZboEuhDiwUIsZgplCfFAHyGsQd57M6uxLrZ5HwOCj6zyqOJ4jgdB04t89/1O/w1cDnyilFU=')

try:
    profile = line_bot_api.get_profile('Ueea1498b70a1795aceac5537f1fa8d11')
    print(profile)
except LineBotApiError as e:
	print(e)
