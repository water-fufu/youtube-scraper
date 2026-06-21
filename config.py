import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY", "")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
TIMEOUT = 15
MAX_SINGLE_QUERY = 50