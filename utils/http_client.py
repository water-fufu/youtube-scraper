import requests
from config import TIMEOUT
from utils.logger import log

# 统一请求头，模拟浏览器，防止API拦截
COMMON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_get(url, params=None, proxies=None):
    try:
        resp = requests.get(
            url=url,
            params=params,
            headers=COMMON_HEADERS,
            timeout=TIMEOUT,
            proxies=proxies
        )
        # 主动抛出非200状态码异常
        resp.raise_for_status()
        return resp
    except requests.exceptions.ProxyError:
        log.error("网络代理连接失败，请检查代理工具是否正常开启")
        raise Exception("代理异常，终止请求")
    except requests.exceptions.ConnectionError:
        log.error("无法连接YouTube API服务器，请检查网络连通性")
        raise Exception("网络连接失败")
    except requests.exceptions.Timeout:
        log.error(f"请求超时，超时阈值：{TIMEOUT}秒")
        raise Exception("请求超时")
    except requests.exceptions.HTTPError as e:
        # 区分403/429/5xx
        if resp.status_code == 403:
            log.error("API密钥无效、权限不足或配额耗尽")
        elif resp.status_code == 429:
            log.error("请求频次超限，请稍后重试")
        elif 500 <= resp.status_code < 600:
            log.error(f"谷歌服务端异常，状态码：{resp.status_code}")
        else:
            log.error(f"接口请求异常：{str(e)}")
        raise Exception("接口返回错误状态码")
    except Exception as e:
        log.error(f"未知网络请求异常：{str(e)}")
        raise Exception("请求失败")


