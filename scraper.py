"""
YouTube 简易爬虫 — 实习入职项目练手版
==========================================
输入关键词 → 调 YouTube API → 提取数据 → 打印 TOP5 → 存 CSV

运行: python scraper.py
学习目标: API 调用、JSON 解析、Pandas 操作、CSV 导出
"""
import requests   # 发送 HTTP 请求的库（给 API 服务器打电话）
import pandas as pd  # 数据表操作库（Excel 能干的它都能干）

# ── 配置 ──
API_KEY = "AIzaSyDtoLfzlE2uRT6R6Nrx6_lloYd2Rsi3kxw"
# API_KEY = 你的"门禁卡"，YouTube 验证后才会返回数据

# YouTube Data API 的请求地址
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"


def search_videos(keyword, max_results=10):
    """
    第1步：按关键词搜索视频，返回每条视频的标题/频道/播放量/点赞数。

    参数:
        keyword: 搜索关键词，如 "Python 爬虫"
        max_results: 最多返回几条

    返回:
        列表，每个元素是一个 dict，包含标题、频道、链接、播放量、点赞数、评论数
    """
    # ── 第一次 API 调用：搜视频 ──
    # params = 传给 API 的"查询条件"，就像在 YouTube 搜索框打字
    search_params = {
        "part": "snippet",   # snippet = 视频基本信息（标题、频道名）
        "q": keyword,        # q = query，搜索关键词
        "type": "video",     # 只搜视频，不要播放列表
        "maxResults": max_results,
        "key": API_KEY,      # 带上"门禁卡"
    }
    # requests.get(): 向 YouTube 发送 HTTP 请求
    search_resp = requests.get(SEARCH_URL, params=search_params, timeout=15)
    # .json(): 把服务器返回的 JSON 字符串转成 Python 字典
    search_data = search_resp.json()

    # 检查是否出错（比如密钥无效）
    if "error" in search_data:
        print(f"API 报错: {search_data['error']['message']}")
        return []

    # items = 搜索命中的视频列表，每个元素是一条视频的简要信息
    items = search_data.get("items", [])
    if not items:
        print(f"没搜到任何关于「{keyword}」的视频")
        return []

    # 过滤掉非视频结果（API 偶尔混入频道/播放列表）
    video_items = [i for i in items if "videoId" in i.get("id", {})]
    if not video_items:
        print(f"关于「{keyword}」未找到视频结果")
        return []

    # 把所有视频 ID 提取出来，拼成逗号分隔的字符串
    # 列表推导式：[操作 for 变量 in 列表] —— 快速生成新列表
    video_ids = [item["id"]["videoId"] for item in video_items]
    ids_string = ",".join(video_ids)  # "id1,id2,id3" 这种格式

    # ── 第二次 API 调用：批量查互动数据 ──
    # snippet 里没播放量，需要调 statistics 接口
    stats_params = {
        "part": "statistics",  # statistics = 播放量、点赞数、评论数
        "id": ids_string,      # 一批视频 ID，逗号隔开
        "key": API_KEY,
    }
    stats_resp = requests.get(VIDEOS_URL, params=stats_params, timeout=15)
    stats_data = stats_resp.json()

    # stats_map: {"视频ID": {"viewCount": ..., "likeCount": ...}} 方便按 ID 取数据
    stats_map = {}
    for v in stats_data.get("items", []):
        vid = v["id"]                     # vid = 视频 ID
        stats = v.get("statistics", {})   # 该视频的互动数据
        stats_map[vid] = stats            # 存入字典，ID 映射到数据

    # ── 合并两次 API 的结果 ──
    results = []  # 最终结果列表，每个元素是一条完整记录
    for item in video_items:  # 注意：遍历过滤后的 video_items，不是原始 items
        vid = item["id"]["videoId"]             # 视频 ID
        snippet = item["snippet"]                # 基本信息
        stats = stats_map.get(vid, {})            # 用 ID 查对应的互动数据

        # 组装成一条清晰的记录
        row = {
            "标题": snippet["title"],
            "频道": snippet["channelTitle"],
            "链接": f"https://youtube.com/watch?v={vid}",
            # int() 把字符串转整数；.get() 取不到就用 0
            "播放量": int(stats.get("viewCount", 0)),
            "点赞数": int(stats.get("likeCount", 0)),
            "评论数": int(stats.get("commentCount", 0)),
        }
        results.append(row)

    return results


def save_and_show(results, keyword):
    """第2步：打印 TOP5 + 全部存 CSV。"""
    if not results:
        return

    # DataFrame = Pandas 的核心数据结构，一张有行有列的二维表
    df = pd.DataFrame(results)

    # 按播放量降序排列
    df = df.sort_values("播放量", ascending=False)

    # ── 打印 TOP5 ──
    print(f"\n{'='*60}")
    print(f"  「{keyword}」YouTube 搜索结果 — TOP5")
    print(f"{'='*60}")
    # .head(5) 取前5行；.iterrows() 逐行遍历，_ 是行号用不上，row 是这行数据
    for i, (_, row) in enumerate(df.head(5).iterrows(), 1):
        print(f"\n {i}. {row['标题'][:60]}")
        # :, 是千位分隔符格式化（1000 → 1,000）
        print(f"    频道: {row['频道']}  |  "
              f"播放: {row['播放量']:,}  |  "
              f"点赞: {row['点赞数']:,}")

    # ── 全部数据存 CSV ──
    csv_name = f"youtube_{keyword}.csv"
    # index=False 不写行号；utf-8-sig 让 Excel 打开不乱码
    df.to_csv(csv_name, index=False, encoding="utf-8-sig")
    print(f"\n 全部 {len(df)} 条已保存到: {csv_name}")


# ═══════════════════════════════════════════════════════════
# 程序入口——直接运行 python scraper.py 就执行这里
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    keyword = input("请输入搜索关键词: ").strip()
    if keyword:
        data = search_videos(keyword)
        save_and_show(data, keyword)
    else:
        print("关键词不能为空")
