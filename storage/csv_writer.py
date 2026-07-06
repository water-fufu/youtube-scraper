import pandas as pd
from config import API_KEY, SEARCH_URL, VIDEOS_URL, TIMEOUT, MAX_SINGLE_QUERY
from utils.logger import log

def save_and_show(results, keyword):
    """第2步：打印 TOP5 + 全部存 CSV。"""
    if not results:
        log.info("无数据可导出CSV")
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
    try:
        df.to_csv(csv_name, encoding="utf-8-sig", index=False)
        log.info(f"数据已保存至文件：{csv_name}")
    except PermissionError:
        log.error("文件写入失败：无文件读写权限，请关闭占用CSV的软件")
    except Exception as e:
        log.error(f"导出CSV异常：{str(e)}")