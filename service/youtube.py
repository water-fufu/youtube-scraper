import requests
from utils.http_client import send_get
from config import API_KEY, SEARCH_URL, VIDEOS_URL, TIMEOUT, MAX_SINGLE_QUERY
from utils.logger import log

def assemble_video_data(vid_list: list):
    result_rows = []
    # 每50个ID切分一批
    batch_size = 50
    for i in range(0, len(vid_list), batch_size):
        batch_ids = vid_list[i:i+batch_size]
        ids_str = ",".join(batch_ids)
        stats_params = {
            "part": "statistics,snippet",
            "id": ids_str,
            "key": API_KEY
        }
        try:
            stats_resp = send_get(VIDEOS_URL, params=stats_params)
            stats_data = stats_resp.json()
        except Exception as e:
            log.error(f"批量查询视频数据失败：{e}")
            continue

        # 组装单条视频数据
        for item in stats_data.get("items", []):
            vid = item.get("id", "")
            snippet = item.get("snippet", {})
            stats = item.get("statistics", {})
            row = {
                "标题": snippet.get("title", "无标题"),
                "频道名": snippet.get("channelTitle", "未知频道"),
                "视频ID": vid,
                "发布时间": snippet.get("publishedAt", ""),
                "播放量": int(stats.get("viewCount", 0)),
                "点赞数": int(stats.get("likeCount", 0)),
                "评论数": int(stats.get("commentCount", 0))
            }
            result_rows.append(row)
    return result_rows

def search_videos(keyword: str, target_count: int = 50):
    # 原有参数校验逻辑保留
    keyword = keyword.strip()
    if not keyword:
        log.error("搜索关键词不能为空")
        return []
    # 限制单次最大采集不超500，避免API配额消耗过大
    if not isinstance(target_count, int) or target_count <= 0 or target_count > 500:
        log.error("目标采集条数必须为1~500之间整数")
        return []

    all_video_ids = []  # 存储所有分页拿到的videoId
    page_token = None   # 分页凭证，初始为空

    # 循环分页，直到收集足够ID或无下一页
    while len(all_video_ids) < target_count:
        search_params = {
            "part": "snippet",
            "q": keyword,
            "type": "video",
            "maxResults": 50,  # 单页拉满上限减少请求次数
            "key": API_KEY
        }
        # 存在下一页token则加入参数
        if page_token:
            search_params["pageToken"] = page_token

        try:
            search_resp = send_get(SEARCH_URL, params=search_params)
            search_data = search_resp.json()
        except Exception as e:
            log.error(f"分页搜索请求失败：{e}")
            break

        page_items = search_data.get("items", [])
        if not page_items:
            log.info("无更多视频数据，终止分页循环")
            break

        # 提取当前页所有视频ID
        for item in page_items:
            vid = item.get("id", {}).get("videoId", "")
            if vid and vid not in all_video_ids:
                all_video_ids.append(vid)
                # 收集数量达标直接跳出循环
                if len(all_video_ids) >= target_count:
                    break

        # 获取下一页凭证，无则结束循环
        page_token = search_data.get("nextPageToken")
        if not page_token:
            log.info("已拉取全部搜索结果，无下一页")
            break

    log.info(f"分页完成，共获取{len(all_video_ids)}个视频ID")
    # 截取用户需要的条数，防止超出目标
    need_ids = all_video_ids[:target_count]
    return assemble_video_data(need_ids)