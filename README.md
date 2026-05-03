# AutoBingWallpaper

一个BingWallpaper的轻量实现。

我喜欢用BingWallpaper来设置我的桌面壁纸，BingWallpaper是一个非常好用的工具，可以自动下载Bing每天的壁纸并设置为桌面壁纸。缺点是软件本体比较臃肿，集成了一些我不想用的功能，而且这是后台常驻软件，然而壁纸切换只要一天一次，完全不需要常驻软件来实现。于是我打算自己实现一个轻量的BingWallpaper，功能就是每天下载Bing的壁纸并设置为桌面壁纸，开机启动后会自动退出。

## ⚠️⚠️⚠️警告：该程序下载的图像仅能用作桌面壁纸，不可用于其他用途

## 目录结构（示例）

```.
├── src                        # 代码文件夹
│   ├── ...
│   └── ...
│
├── .gitignore                 # Git忽略文件
├── .pre-commit-config.yaml    # pre-commit配置文件
├── dev.py                     # 开发脚本，集成常用指令
├── pyproject.toml             # Python项目配置文件
├── README.md                  # 项目说明文件
└── uv.lock                    # Python依赖锁文件
```

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
