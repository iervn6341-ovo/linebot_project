import requests
import json
import os
import threading
import types
import time
import warnings

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler, LineBotSdkDeprecatedIn30
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from urllib.request import urlretrieve