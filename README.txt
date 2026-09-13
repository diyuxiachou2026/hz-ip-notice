怀化知产 · 官网通知每日自动抓取（GitHub 版）
====================================================

一、这个仓库是干什么的
  每天自动抓取以下官网的通知公告：
    1. 国家知识产权局 · 通知公告
    2. 湖南省市场监管局 · 动态
    3. 怀化市市场监管局 · 通知公告栏目（两个）
  抓取后按关键词过滤（专利、商标、地理标志等），生成 ip-notice.json，
  由 GitHub 定时任务自动提交回仓库，再通过 GitHub Pages 供手机 APP 读取。

二、仓库里的文件
  fetch.py            抓取脚本（无需安装任何依赖，Python 标准库即可）
  README.txt          本说明
  .github/workflows/  定时任务配置（按操作手册在网页上手动创建）

三、怎么用
  1. 在 GitHub 网页创建公开仓库（如 hz-ip-notice）
  2. 上传 fetch.py（网页"Add file → Upload files"直接拖入）
  3. 手动创建定时任务文件：
     "Add file → Create new file"，文件名填：
     .github/workflows/fetch.yml
     内容见操作手册附录（约 20 行，直接复制粘贴）
  4. 开启定时任务写权限：仓库 Settings → Actions → General →
     Workflow permissions → 选 "Read and write permissions" → Save
  5. 手动运行一次测试：仓库 Actions 页 → 左侧工作流 → Run workflow
  6. 开启网页空间：仓库 Settings → Pages → Source 选 Branch →
     main / (root) → Save，等待约 1 分钟
  7. 验证：浏览器打开
     https://你的用户名.github.io/hz-ip-notice/ip-notice.json
     能看到 JSON 且 items 非空即成功

四、两个可用的读取地址（把其中任一个发给开发侧接入 APP）
  地址1（GitHub Pages 官方）：
    https://你的用户名.github.io/hz-ip-notice/ip-notice.json
  地址2（国内 CDN 加速，jsDelivr）：
    https://cdn.jsdelivr.net/gh/你的用户名/hz-ip-notice@main/ip-notice.json

五、修改抓取内容或时间
  改关键词：编辑 fetch.py 顶部 KEYWORDS 列表，提交后自动生效
  改时间：编辑 .github/workflows/fetch.yml 里 cron 表达式
    （当前每天 8:00 北京时间，即 0 0 * * * UTC）

六、费用
  完全免费、永久免费：GitHub 公开仓库的定时任务免费额度无限，
  GitHub Pages 网页空间免费且流量无限。

开发者：怀化市市场监督管理局 知识产权促进运用科 孙艳华
