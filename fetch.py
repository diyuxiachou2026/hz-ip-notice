# -*- coding: utf-8 -*-
# =====================================================
#  怀化知产掌上工作台 · 官网通知每日自动抓取脚本
#  运行环境：GitHub Actions（Python 3，仅用标准库，无第三方依赖）
#  作用：每天定时抓取官网列表页 -> 关键词过滤 -> 生成 ip-notice.json
#  生成文件会由定时任务自动提交回仓库，并通过 GitHub Pages 提供访问
# =====================================================
import json, re, datetime, urllib.request, gzip

# ===== 关键词：只保留与知识产权相关的条目（想加词就加在列表里）=====
KEYWORDS = ["专利", "商标", "地理标志", "集成电路布图", "知识产权",
            "质押融资", "转让许可", "开放许可", "驰名商标", "高价值", "数据知识产权"]

# ===== 抓取源：国家局 + 省局 + 怀化市局（两个栏目）=====
# filter: True=按关键词过滤（适合可能混有他类内容的栏目）
#         False=全部收录（官方知识产权栏目，标题即相关，直接全收更全）
SOURCES = [
    {"name": "国家局", "url": "https://www.cnipa.gov.cn/col/col74/index.html", "filter": False},
    {"name": "省局", "url": "https://amr.hunan.gov.cn/amr/zwx/", "filter": False},
    {"name": "市局", "url": "https://www.huaihua.gov.cn/amr/c100640/list.shtml", "filter": True},
    {"name": "市局", "url": "https://www.huaihua.gov.cn/amr/c100647/list.shtml", "filter": True},
]

def fetch(url):
    def _once(context):
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate"})
        r = urllib.request.urlopen(req, timeout=20, context=context)
        raw = r.read()
        if r.headers.get("Content-Encoding", "") == "gzip":
            raw = gzip.decompress(raw)
        return raw.decode("utf-8", "ignore")
    try:
        return _once(None)
    except Exception:
        import ssl
        return _once(ssl._create_unverified_context())

def parse(page_url, html_text, need_filter):
    items = []
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)</a>', html_text):
        href, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        txt = re.sub(r"\s+", " ", txt).strip()
        if len(txt) < 6 or len(txt) > 60:
            continue
        if need_filter and not any(k in txt for k in KEYWORDS):
            continue
        dm = re.search(r"\d{4}-\d{2}-\d{2}", txt)
        if href.startswith("http"):
            u = href
        elif href.startswith("/"):
            u = "https://" + page_url.split("/")[2] + href
        else:
            u = page_url.rsplit("/", 1)[0] + "/" + href
        items.append({"t": txt, "d": dm.group(0) if dm else "", "u": u})
    return items

def main():
    seen, out = set(), []
    for s in SOURCES:
        try:
            for it in parse(s["url"], fetch(s["url"]), s.get("filter", True))[:40]:
                if it["t"] in seen:
                    continue
                seen.add(it["t"])
                it["src"] = s["name"]
                out.append(it)
            print("OK", s["name"], s["url"])
        except Exception as e:
            print("FAIL", s["name"], s["url"], str(e)[:120])
    out = out[:80]
    data = {"updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "items": out}
    with open("ip-notice.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("DONE total", len(out))

if __name__ == "__main__":
    main()
