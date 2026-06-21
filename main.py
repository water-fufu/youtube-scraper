# main.py
from config import API_KEY, SEARCH_URL, VIDEOS_URL, TIMEOUT
from service.youtube import search_videos
from storage.csv_writer import save_and_show

if __name__ == "__main__":
    keyword = input("请输入搜索关键词: ").strip()
    if keyword:
        data = search_videos(keyword)
        save_and_show(data, keyword)
    else:
        print("关键词不能为空")