"""
本脚本旨在集成常用的的项目开发指令。
"""

import sys
import subprocess
from pathlib import Path
from functools import wraps
from time import perf_counter_ns as get_time_ns

import rich
import rich.style
import rich.console
import typer

CWD = Path(__file__).parent
CONSOLE = rich.console.Console()

NORMAL_STYLE = rich.style.Style(color="white")
ERROR_STYLE = rich.style.Style(color="red")
SUCCESSFUL_STYLE = rich.style.Style(color="green")
WARNING_STYLE = rich.style.Style(color="yellow")
INFO_STYLE = rich.style.Style(color="blue")
DEBUG_STYLE = rich.style.Style(color="cyan")
TITLE_STYLE = rich.style.Style(color="deep_pink4", bold=True)
COMMENT_STYLE = rich.style.Style(color="grey50")


def prints(*msg_list: tuple[str, rich.style.Style]) -> None:
    """使用 rich 打印多条带有样式的消息"""
    for msg, style in msg_list:
        CONSOLE.print(msg, style=style, end="")
    print("")


def auto_timeunit(time_ns: int) -> str:
    """自动转换时间单位，返回带有单位的字符串"""
    elapsed_time: float = float(time_ns)

    if elapsed_time < 1000:
        return f"{elapsed_time:.2f} ns"
    elapsed_time /= 1000
    if elapsed_time < 1000:
        return f"{elapsed_time:.2f} μs"
    elapsed_time /= 1000
    if elapsed_time < 1000:
        return f"{elapsed_time:.2f} ms"
    elapsed_time /= 1000
    if elapsed_time < 60:
        return f"{elapsed_time:.2f} s"
    elapsed_time /= 60
    if elapsed_time < 60:
        return f"{elapsed_time:.2f} min"
    elapsed_time /= 60
    return f"{elapsed_time:.2f} h"


def cmd_run(
    cmd: list[str],
    capture_output: bool = False,
    error_on_output: bool = False,
    cwd: Path = CWD,
) -> str:
    """模拟命令行终端运行命令"""
    if error_on_output:
        capture_output = True

    norm_cmd = [str(i) for i in cmd]
    prints(
        (r"\[run] ", TITLE_STYLE),
        (f"[cyan]{' '.join(norm_cmd)}[/]", DEBUG_STYLE),
    )

    result = subprocess.run(
        norm_cmd,
        stdout=subprocess.PIPE if capture_output else sys.stdout,
        stderr=subprocess.STDOUT,
        text=capture_output,
        cwd=cwd,
        check=True,
    )

    if result.stdout:
        print(result.stdout, end="", flush=True)

    if (error_on_output and result.stdout) and not result.returncode:
        result.returncode = 1

    result.check_returncode()
    return result.stdout.strip() if capture_output else ""


app = typer.Typer(
    help="开发相关的命令集合",
    add_completion=False,
    no_args_is_help=True,
)


def app_command(
    typer_app: typer.Typer = app,
    name: str | None = None,
    rich_help_panel: str | None = None,
):
    """装饰器，用于包装命令函数，添加统一的日志输出和错误处理"""

    def command(func):
        @typer_app.command(name=name, rich_help_panel=rich_help_panel)
        @wraps(func)
        def command_func(*args, **kwargs):
            func_name = name if name is not None else func.__name__
            start_time = get_time_ns()
            prints(
                (r"\[dev.py] ", TITLE_STYLE),
                ("运行命令 ", NORMAL_STYLE),
                (f"{func_name}", INFO_STYLE),
            )

            try:
                result = func(*args, **kwargs)
            except subprocess.CalledProcessError:
                prints(
                    (r"\[dev.py] ", TITLE_STYLE),
                    (f'命令 "{func_name}" 运行失败，请检查错误信息', ERROR_STYLE),
                )
                sys.exit(1)
            except KeyboardInterrupt:
                prints(
                    (r"\[dev.py] ", TITLE_STYLE),
                    (f'命令 "{func_name}" 被用户中断', WARNING_STYLE),
                )
                sys.exit(1)
            except Exception as e:
                prints(
                    (r"\[dev.py] ", TITLE_STYLE),
                    (f'命令 "{func_name}" 运行失败，发生错误: {e}', ERROR_STYLE),
                )
                sys.exit(1)

            end_time = get_time_ns()
            prints(
                (r"\[dev.py]", TITLE_STYLE),
                (
                    f" 命令 {func_name} 执行成功,",
                    SUCCESSFUL_STYLE,
                ),
                (
                    f" 耗时：[grey50]{auto_timeunit(end_time - start_time)}[/]",
                    COMMENT_STYLE,
                ),
            )
            return result

        return command_func

    return command


@app_command(app)
def init():
    """初始化项目"""
    prints(
        (r"\[pre-commit] ", TITLE_STYLE),
        ("创建预提交钩子", NORMAL_STYLE),
    )
    try:
        cmd_run(["uv", "run", "pre-commit", "install"])
    except subprocess.CalledProcessError as e:
        prints(
            (r"\[pre-commit] ", TITLE_STYLE),
            ("预提交钩子创建失败，请检查错误信息", ERROR_STYLE),
        )
        raise e


@app_command(app)
def check():
    """代码审查"""
    prints(
        (r"\[ruff] ", TITLE_STYLE),
        ("格式化代码", NORMAL_STYLE),
    )
    try:
        cmd_run(["uv", "run", "ruff", "format"])
    except subprocess.CalledProcessError as e:
        prints(
            (r"\[ruff] ", TITLE_STYLE),
            ("代码格式化失败，请检查错误信息", ERROR_STYLE),
        )
        raise e

    prints(
        (r"\[ruff] ", TITLE_STYLE),
        ("分析代码质量", NORMAL_STYLE),
    )
    try:
        cmd_run(["uv", "run", "ruff", "check", "--fix"])
    except subprocess.CalledProcessError as e:
        prints(
            (r"\[ruff] ", TITLE_STYLE),
            ("代码质量分析失败，请检查错误信息", ERROR_STYLE),
        )
        raise e

    prints(
        (r"\[ty] ", TITLE_STYLE),
        ("静态类型检查", NORMAL_STYLE),
    )
    try:
        cmd_run(["uv", "run", "ty", "check"])
    except subprocess.CalledProcessError as e:
        prints(
            (r"\[ty] ", TITLE_STYLE),
            ("静态类型检查失败，请检查错误信息", ERROR_STYLE),
        )
        raise e


@app_command(app)
def build():
    """构建项目"""
    from utils.get_version import get_version

    prints(
        (r"\[dev.py] ", TITLE_STYLE),
        ("准备元数据", NORMAL_STYLE),
    )

    version = get_version().split(".")
    if len(version) < 3:
        prints(
            (r"\[dev.py] ", TITLE_STYLE),
            ("版本号格式不正确，应该为 major.minor.patch", ERROR_STYLE),
        )
        raise ValueError("版本号格式不正确，应该为 major.minor.patch")

    version_file_template = CWD / "version-file-template.txt"
    version_file_content = version_file_template.read_text(encoding="utf-8").strip()
    version_file_content = version_file_content.format(
        major0=version[0],
        major1=version[0],
        minor0=version[1],
        minor1=version[1],
        patch0=version[2],
        patch1=version[2],
        version0=".".join(version),
        version1=".".join(version),
    )
    version_file = CWD / "version-file.txt"
    version_file.write_text(version_file_content, encoding="utf-8")

    dist_dir = CWD / "dist"
    if dist_dir.exists():
        for file in dist_dir.iterdir():
            if file.is_file():
                file.unlink()

    prints(
        (r"\[pyinstaller] ", TITLE_STYLE),
        ("使用 PyInstaller 构建项目", NORMAL_STYLE),
    )

    try:
        cmd_run(
            [
                "uv",
                "run",
                "pyinstaller",
                "-w",
                "-F",
                "--name",
                "每日bing壁纸",
                "-i",
                "assets/icon.ico",
                "src/main.py",
                "--version-file",
                "version-file.txt",
            ]
        )
    except subprocess.CalledProcessError as e:
        prints(
            (r"\[pyinstaller] ", TITLE_STYLE),
            ("项目构建失败，请检查错误信息", ERROR_STYLE),
        )
        raise e

    if version_file.exists():
        version_file.unlink()
    if (CWD / "main.spec").exists():
        (CWD / "main.spec").unlink()

    exe = dist_dir / "每日bing壁纸.exe"
    if exe.exists():
        prints(
            (r"\[dev.py] ", TITLE_STYLE),
            ("项目构建成功，生成的可执行文件位于 ", NORMAL_STYLE),
            (f"{exe}", INFO_STYLE),
        )
    else:
        prints(
            (r"\[dev.py] ", TITLE_STYLE),
            ("项目构建失败，未找到生成的可执行文件", ERROR_STYLE),
        )
        raise FileNotFoundError("项目构建失败，未找到生成的可执行文件")


if __name__ == "__main__":
    app()
