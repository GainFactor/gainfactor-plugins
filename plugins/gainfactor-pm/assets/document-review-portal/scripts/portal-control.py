#!/usr/bin/env python3
"""Build, open, and stop a local GainFactor document portal."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path


STATE_DIRECTORY = ".portal-runtime"
STATE_FILE = "server.json"
BUILD_STAMP = "build.stamp"
LOG_FILE = "portal.log"


def notify(title: str, message: str) -> None:
    print(f"{title}: {message}")
    if sys.platform == "darwin" and shutil.which("osascript"):
        safe_title = title.replace('"', '\\"')
        safe_message = message.replace('"', '\\"')
        subprocess.run(
            ["osascript", "-e", f'display alert "{safe_title}" message "{safe_message}"'],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def runtime_paths(portal: Path) -> tuple[Path, Path, Path]:
    runtime = portal / STATE_DIRECTORY
    runtime.mkdir(exist_ok=True)
    return runtime / STATE_FILE, runtime / BUILD_STAMP, runtime / LOG_FILE


def read_state(path: Path) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def process_is_portal_server(pid: int, portal: Path) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    if sys.platform != "darwin":
        return True
    completed = subprocess.run(
        ["ps", "-p", str(pid), "-o", "command="],
        capture_output=True,
        text=True,
        check=False,
    )
    command = completed.stdout.strip()
    return "serve" in command and str(portal / "out") in command


def port_is_open(port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.3):
            return True
    except OSError:
        return False


def choose_port() -> int:
    preferred = int(os.environ.get("GAINFACTOR_PORTAL_PORT", "3210"))
    for port in range(preferred, preferred + 100):
        with socket.socket() as candidate:
            try:
                candidate.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError("3210–3309 端口均被占用")


def newest_source_mtime(portal: Path) -> float:
    roots = ["app", "components", "content", "lib", "public"]
    files = [portal / "package.json", portal / "pnpm-lock.yaml", portal / "next.config.mjs"]
    for root_name in roots:
        root = portal / root_name
        if root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file())
    return max((path.stat().st_mtime for path in files if path.exists()), default=0)


def build_is_current(portal: Path, stamp: Path) -> bool:
    index = portal / "out/index.html"
    return index.is_file() and stamp.is_file() and stamp.stat().st_mtime >= newest_source_mtime(portal)


def package_command() -> list[str]:
    if shutil.which("pnpm"):
        return ["pnpm"]
    if shutil.which("corepack"):
        return ["corepack", "pnpm"]
    raise RuntimeError("未找到 pnpm 或 corepack。请先安装 Node.js，或联系研发同学完成首次环境配置。")


def ensure_build(portal: Path, stamp: Path, log_path: Path) -> None:
    if build_is_current(portal, stamp):
        return
    manager = package_command()
    print("首次打开或内容已有更新，正在准备文档门户……")
    with log_path.open("a", encoding="utf-8") as log:
        if not (portal / "node_modules/.bin/serve").is_file():
            subprocess.run(
                [*manager, "install", "--frozen-lockfile"],
                cwd=portal,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=True,
            )
        subprocess.run(
            [*manager, "run", "build"],
            cwd=portal,
            stdout=log,
            stderr=subprocess.STDOUT,
            check=True,
        )
    stamp.touch()


def open_browser(url: str) -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", url], check=False)
    else:
        webbrowser.open(url)


def open_portal(portal: Path) -> int:
    state_path, stamp_path, log_path = runtime_paths(portal)
    state = read_state(state_path)
    if state:
        pid = int(state.get("pid", 0))
        port = int(state.get("port", 0))
        if process_is_portal_server(pid, portal) and port_is_open(port):
            url = f"http://127.0.0.1:{port}"
            open_browser(url)
            print(f"文档门户已经运行：{url}")
            return 0
        state_path.unlink(missing_ok=True)

    try:
        ensure_build(portal, stamp_path, log_path)
        port = choose_port()
        serve = portal / "node_modules/.bin/serve"
        if not serve.is_file():
            raise RuntimeError("静态服务器依赖缺失，请删除 node_modules 后重新打开。")
        log = log_path.open("a", encoding="utf-8")
        process = subprocess.Popen(
            [str(serve), str(portal / "out"), "-l", f"tcp://127.0.0.1:{port}", "--no-clipboard"],
            cwd=portal,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        state_path.write_text(
            json.dumps({"pid": process.pid, "port": port}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        for _ in range(40):
            if port_is_open(port):
                url = f"http://127.0.0.1:{port}"
                open_browser(url)
                print(f"文档门户已打开：{url}")
                return 0
            if process.poll() is not None:
                break
            time.sleep(0.25)
        raise RuntimeError(f"门户启动失败，请查看日志：{log_path}")
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        state_path.unlink(missing_ok=True)
        notify("无法打开文档门户", str(error))
        return 1


def stop_portal(portal: Path) -> int:
    state_path, _, _ = runtime_paths(portal)
    state = read_state(state_path)
    if not state:
        print("文档门户当前没有运行。")
        return 0
    pid = int(state.get("pid", 0))
    if not process_is_portal_server(pid, portal):
        state_path.unlink(missing_ok=True)
        print("文档门户当前没有运行。")
        return 0
    try:
        os.killpg(pid, signal.SIGTERM)
    except OSError:
        os.kill(pid, signal.SIGTERM)
    state_path.unlink(missing_ok=True)
    print("文档门户已关闭。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="打开或关闭 GainFactor 文档门户")
    parser.add_argument("action", choices=("open", "stop"))
    parser.add_argument("portal", type=Path)
    args = parser.parse_args()
    portal = args.portal.resolve()
    if not (portal / ".gainfactor-documents.json").is_file():
        notify("无法操作文档门户", f"目录不是 GainFactor 文档门户：{portal}")
        return 1
    return open_portal(portal) if args.action == "open" else stop_portal(portal)


if __name__ == "__main__":
    raise SystemExit(main())
