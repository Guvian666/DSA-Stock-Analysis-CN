# DSA 股票智能分析 · 中文本地化定制版

基于开源项目 [ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) **v3.35.0** 的 Windows 桌面端中文本地化定制版本。

> 本仓库**不含**上游源码，只包含「本地化改动 + 打包脚本 + 中文说明书」。
> 可执行成品（安装包）在 [Releases](../../releases) 页，仓库里不放 240MB 二进制。

---

## 这个仓库解决什么问题

上游 v3.35.0 的界面翻译其实是**完整的**（中文字典 985 条 / 英文字典 984 条），
但有两类英文会露在外面：

1. **Electron 外壳**：默认菜单栏 `File / Edit / View / Window / Help`，以及启动页
   `Preparing backend and loading UI...` 这段文案，都写死在 `app.asar` 里，不在前端字典里。
2. **前端字典的 8 条中文值**仍是英文：`Usage`、`Breakdown`、`Task`、`Trace` 等。

本定制版把这两类全部改成中文，并加入作者信息与免责声明面板。

## 改动清单

| # | 位置 | 改动 |
|---|------|------|
| 1 | `app.asar` → `main.js` | 新增 `Menu` 依赖；重建中文菜单（文件/编辑/视图/窗口/帮助）；新增 `showAboutDialog()`；`whenReady` 时安装菜单 |
| 2 | `app.asar` → `renderer/loading.html` | 启动页整页汉化 + 作者署名 + 免责声明 + 上游署名 |
| 3 | 前端 `index-*.js` | 8 条中文侧字典项由英文改为中文（见 `scripts/apply_frontend_localization.py`） |

主进程的完整差异见 [`patches/main.js.patch`](patches/main.js.patch)（131 行，新增 110 行）。

## 安装（普通用户）

1. 到 [Releases](../../releases) 下载 `DSA-Stock-Analysis-CN-v3.35.0-setup.exe`（240 MB）
2. 双击安装（默认当前用户目录，**不需要管理员权限**）
3. 首次启动等 10~20 秒
4. 进「系统设置 → AI 模型」填一个模型 Key（推荐 DeepSeek），点「测试渠道」通过即可用

详细说明见 [`docs/使用说明.pdf`](docs/使用说明.pdf)（12 章，含故障对照表）。

## 自行构建安装包

需要：Node.js 18+、能访问 GitHub Releases 的网络环境。

```bash
# 1. 取官方免安装包（v3.35.0）
#    daily-stock-analysis-windows-noinstall-v3.35.0.zip

# 2. 解压到 payload/，并用 asar 解包外壳
npx @electron/asar extract payload/resources/app.asar app_unpacked

# 3. 打主进程补丁
cd app_unpacked
git apply ../patches/main.js.patch          # 或手动对照 patch 修改
cp ../patches/loading.html renderer/loading.html
cd ..

# 4. 打前端字典补丁
python scripts/apply_frontend_localization.py \
    payload/resources/backend/stock_analysis/_internal/static/assets

# 5. 重新打包外壳
npx @electron/asar pack app_unpacked payload/resources/app.asar

# 6. 清理个人数据（重要！不要把自己的 .env / data / logs 打进去）
rm -rf payload/data payload/logs payload/.env

# 7. 生成安装包
npx electron-builder --prepackaged payload --win nsis --x64
```

`build/electron-builder.json` 是本项目使用的完整构建配置（per-user 安装、可选目录、中文快捷方式）。

### 两个必踩的坑

- `electron-builder` 必须放在 **devDependencies**，放 `dependencies` 会直接报错退出。
- 用 `--prepackaged` 时必须显式指定 `build.electronVersion`（本项目为 `20.18.0`），
  否则报 `Cannot compute electron version from installed node modules`。

## 许可与署名

- 上游项目：[ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis)，**MIT License**，版权归原作者。
- 本仓库的本地化改动同样以 MIT 发布，见 [`LICENSE`](LICENSE)。
- 依据 MIT 协议，再分发时必须保留原始版权声明；本项目在「关于」面板与安装包内均保留了对上游的署名。
- 本项目**不是**上游官方版本，上游作者不对本定制版负责。

## 免责声明

本软件仅供个人学习与研究使用，**不构成任何投资建议**。股市有风险，投资需谨慎。
因使用本软件产生的任何直接或间接损失，作者不承担任何责任。