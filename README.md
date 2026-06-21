# YouTube 视频信息采集工具

基于 YouTube Data API 的视频信息搜索与导出工具，按关键词搜索视频并保存为 CSV。

## 项目结构

```
├── main.py                  # 入口（交互式关键词搜索）
├── scraper.py               # 核心采集逻辑
├── config.py                # API 配置
├── service/youtube.py       # YouTube API 调用
├── storage/csv_writer.py    # CSV 输出
├── requirements.txt         # 依赖
└── youtube_原神.csv         # 示例输出
```

## 环境依赖

```bash
pip install -r requirements.txt
```

## 配置

在 .env 或 config.py 中设置 YouTube Data API Key。

## 使用

```bash
python main.py
```

输入搜索关键词，自动获取视频标题、频道、发布时间、播放量等信息并导出 CSV。
