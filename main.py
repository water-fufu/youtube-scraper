# main.py
from config import API_KEY, SEARCH_URL, VIDEOS_URL, TIMEOUT
from service.youtube import search_videos
from storage.csv_writer import save_and_show

if __name__ == "__main__":
    keyword = input("请输入搜索关键词: ").strip()
    if keyword:
        try:
            num = int(input("请输入需要采集的视频条数(1~500): ").strip())
        except ValueError:
            log.warning("输入条数非法，默认采集50条")
            num = 50
        data = search_videos(keyword, target_count=num)
        save_and_show(data, keyword)
    else:
        log.error("关键词不能为空")