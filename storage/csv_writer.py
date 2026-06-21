import pandas as pd
from config import API_KEY, SEARCH_URL, VIDEOS_URL, TIMEOUT, MAX_SINGLE_QUERY

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