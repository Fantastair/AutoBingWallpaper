# AutoBingWallpaper

一个 BingWallpaper 的轻量实现，支持 **Windows** 和 **Linux**。

我喜欢用 BingWallpaper 来设置我的桌面壁纸，BingWallpaper 是一个非常好用的工具，可以自动下载 Bing 每天的壁纸并设置为桌面壁纸。缺点是软件本体比较臃肿，集成了一些我不想用的功能，而且这是后台常驻软件，然而壁纸切换只要一天一次，完全不需要常驻软件来实现。于是我打算自己实现一个轻量的 BingWallpaper，功能就是每天下载 Bing 的壁纸并设置为桌面壁纸，开机启动后会自动退出。

## ⚠️⚠️⚠️警告：该程序下载的图像仅能用作桌面壁纸，不可用于其他用途

## 支持的平台

| 平台 | 状态 |
| ---- | ---- |
| Windows 10/11 | ✅ 完全支持 |
| Linux (GNOME / KDE / XFCE / Cinnamon / MATE / Budgie / Unity / i3) | ✅ 自动检测桌面环境 |

> Linux 下的桌面环境通过 `XDG_CURRENT_DESKTOP` 环境变量自动检测，无需手动配置。

## 目录结构

```.
├── assets                       # 资源文件夹
│   ├── icon.ico                 # Windows 图标文件
│   └── icon.svg                 # Linux 图标文件
│
├── src                          # 代码文件夹
│   └── main.py                  # 主文件
│
├── utils                        # 工具文件夹
│   └── get_version.py           # 获取版本号的工具文件
│
├── .gitignore                   # Git忽略文件
├── .pre-commit-config.yaml      # pre-commit配置文件
├── dev.py                       # 开发脚本，集成常用指令
├── LICENSE                      # 许可证文件
├── pyproject.toml               # Python项目配置文件
├── README.md                    # 项目说明文件
├── uv.lock                      # Python依赖锁文件
└── version-file-template.txt    # 版本文件模板
```

## 许可证

本项目遵循 MIT 许可证（MIT License）。有关完整许可证文本，请参阅仓库根目录下的 [LICENSE](./LICENSE) 文件。

简要许可说明：

- 允许免费使用、复制、修改、合并、发布、分发、再许可和/或出售本软件的副本。
- 使用时须在所有副本或实质性部分中包含原始版权声明和本许可声明。
- 本软件按“原样”提供，不附带任何明示或暗示的担保，作者不对因软件引起的任何索赔、损害或其他责任承担责任。

## 获取项目

```bash
git clone https://github.com/Fantastair/AutoBingWallpaper.git
```

## 环境配置

本项目使用 [`uv`](https://docs.astral.org.cn/uv/) 管理，为确保项目的可复现性，请按照以下步骤配置环境：

### 1. 安装 [`uv`](https://docs.astral.org.cn/uv/)

- `Windows`

    > 建议获取管理员权限后运行

    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

- `MacOS / Linux`

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    如果系统没有 curl，可以使用 wget：

    ```bash
    wget -qO- https://astral.sh/uv/install.sh | sh
    ```

> 更多安装方式可以参考
> [`uv` 官方文档](https://docs.astral.sh/uv/getting-started/installation/) /
> [中文翻译版本](https://docs.astral.org.cn/uv/getting-started/installation/)。

完成之后，可能需要重启终端以使用新的环境变量配置。

无论使用何种方式安装，都需要确保可以直接使用 `uv ...` 命令。

可以使用下面的命令检测 `uv ...` 命令是否可用：

```bash
uv --version
```

### 2. 安装 `python`

> 下载 `python` 可能较慢，[`uv`](https://docs.astral.org.cn/uv/) 支持换源，但是国内镜像源暂时没有很好的兼容，
> 这一步可以尝试手动下载对应版本的 `python`

```bash
uv python install
```

由于一个系统中允许存在多个 `python` 环境，因此不要求能够直接使用 `python` 命令，只要
[`uv`](https://docs.astral.org.cn/uv/) 能够找到安装的 `python` 即可：

```bash
uv python list --only-installed
```

检查上面命令的输出中有无对应的 `python` 版本，如果有，则可以继续下一步。

### 3. 初始化项目

使用项目的开发脚本 [`dev.py`](./dev.py) 来执行初始化操作（有关
[`dev.py`](./dev.py) 的更多信息，请参见 [开发命令](#开发命令)）：

```bash
uv run dev.py init
```

## 开发命令

[`dev.py`](./dev.py) 是一个开发脚本，集成了开发需要用到的指令。

可以直接使用 `uv run` 运行脚本，也可以使用激活了项目虚拟环境的 `python` 运行：

```bash
uv run dev.py [OPTIONS] COMMAND [ARGS]...
# python dev.py [OPTIONS] COMMAND [ARGS]...
```

### 获取指令帮助

使用 `--help` 参数可以获取指令的帮助信息：

```bash
uv run dev.py --help
```

或者不带参数也可以显示帮助信息：

```bash
uv run dev.py
```

也可以在子命令后面加上 `--help` 来获取子命令的帮助信息：

```bash
uv run dev.py check --help
```

### 初始化项目

```bash
uv run dev.py init
```

初始化包含以下步骤：

- 创建虚拟环境，位于 `.venv/` 目录
- 安装项目依赖
- 安装 `pre-commit` 钩子

### 代码审查指令

```bash
uv run dev.py check
```

代码审查包含以下部分：

- 格式化代码：使用 `ruff` 的 `format` 命令来格式化代码。
- 分析代码质量：使用 `ruff` 的 `check` 命令来分析代码质量，并尝试修复可修复的问题。
- 静态类型检查：使用 `ty` 的 `check` 命令来进行静态类型检查。

> 注意：如果代码审查不通过，会阻止进行 `git commit` 相关操作。

### 构建项目

```bash
uv run dev.py build
```

使用 `pyinstaller` 来构建项目，构建完成后会在 `dist/` 目录下生成可执行文件。

## 自动运行

程序切换完壁纸后就会退出，无后台驻留。

### Windows

- **设为开机启动**：

  按下 `Win + R`，输入 `shell:startup`，回车，打开启动文件夹。将可执行文件的快捷方式放入该文件夹中即可。

- **定时任务**（如果不是每天都开关机）：

  1. 打开任务计划程序：按下 `Win + S`，输入 `任务计划程序`，回车。
  2. 创建基本任务：在右侧操作栏中点击 `创建基本任务...`。
  3. 设置任务名称和描述：输入任务的名称（例如 "AutoBingWallpaper"）和描述，然后点击 `下一步`。
  4. 选择触发器：选择 `每天`，然后点击 `下一步`。
  5. 设置开始时间：选择任务开始的日期和时间，然后点击 `下一步`。
  6. 选择操作：选择 `启动程序`，然后点击 `下一步`。
  7. 选择程序：点击 `浏览...`，找到项目的可执行文件，选择它，然后点击 `下一步`。
  8. 完成任务：检查任务的设置是否正确，然后点击 `完成`。

### Linux

- **设为开机启动（systemd 用户服务）**：

  创建 `~/.config/systemd/user/autobingwallpaper.service`：

  ```ini
  [Unit]
  Description=Auto Bing Wallpaper

  [Service]
  Type=oneshot
  ExecStart=/usr/bin/python3 /path/to/AutoBingWallpaper/src/main.py

  [Install]
  WantedBy=default.target
  ```

  然后启用服务：

  ```bash
  systemctl --user enable autobingwallpaper.service
  ```

- **定时任务（cron）**：

  使用 `crontab -e` 添加每天定时运行：

  ```cron
  0 9 * * * /usr/bin/python3 /path/to/AutoBingWallpaper/src/main.py
  ```

  上面配置表示每天 9:00 执行一次。
