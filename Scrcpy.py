# 无线 Scrcpy 启动脚本：通过 ADB 连接远程设备，然后启动 Scrcpy 投屏。

# 导入模块
import signal
import sys
import subprocess

# ==================== 全局配置 ====================

# --- 设备连接参数 ---
DEVICE_ADDRESS = "100.64.0.3:43355"

# --- Scrcpy 参数 ---
SCRCPY_VIDEO_BITRATE = "4M"
SCRCPY_MAX_FPS = "30"
SCRCPY_VIDEO_CODEC = "h265"
SCRCPY_AUDIO_CODEC = "opus"
SCRCPY_KEYBOARD = "uhid"

# --- 消息常量 ---
MSG_TITLE = "无线 Scrcpy 启动工具"
MSG_CONNECTING = "正在通过 ADB 连接设备 {} ..."
MSG_CONNECT_OK = "ADB 连接成功。"
MSG_CONNECT_FAIL = "ADB 连接失败（设备可能已连接，继续执行）。"
MSG_CHECKING_DEVICES = "正在检查已连接设备..."
MSG_DEVICE_FOUND = "目标设备已就绪: {}"
MSG_DEVICE_NOT_FOUND = "警告：未在已连接设备列表中找到目标设备，但将继续尝试启动。"
MSG_LAUNCHING_SCRCPY = "正在启动 Scrcpy..."
MSG_SCRCPY_EXIT = "Scrcpy 已退出。"
MSG_SCRCPY_ERROR = "Scrcpy 启动失败或已退出（返回码: {}）。"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# ==================== 中断处理 ====================

_quit_requested = False


def _on_quit_signal(signum, frame):
    global _quit_requested
    _quit_requested = True
    raise KeyboardInterrupt()


def _init_quit_handler():
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, _on_quit_signal)


# ==================== 处理函数 ====================

def run_adb_connect(address):
    """通过 ADB 连接到指定地址的设备。返回 True 表示返回码为 0。"""
    print(MSG_CONNECTING.format(address))
    result = subprocess.run(
        ["adb", "connect", address],
        capture_output=True,
        text=True,
        timeout=15,
    )
    print("    " + result.stdout.strip())
    if result.returncode == 0:
        print(MSG_CONNECT_OK)
        return True
    else:
        if result.stderr:
            print("    " + result.stderr.strip())
        print(MSG_CONNECT_FAIL)
        return False


def run_adb_devices():
    """列出已连接的 ADB 设备。返回 stdout 字符串。"""
    print(MSG_CHECKING_DEVICES)
    result = subprocess.run(
        ["adb", "devices"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    output = result.stdout.strip()
    print(output)
    return output


def is_device_online(address, devices_output):
    """根据 adb devices 输出判断目标设备是否在线。"""
    for line in devices_output.splitlines():
        if line.startswith(address) and "\tdevice" in line:
            return True
    return False


def run_scrcpy(address):
    """启动 Scrcpy 连接指定设备。此函数会阻塞直到 Scrcpy 退出。"""
    print(MSG_LAUNCHING_SCRCPY)
    cmd = [
        "scrcpy",
        "-s", address,
        "--video-bit-rate", SCRCPY_VIDEO_BITRATE,
        "--max-fps", SCRCPY_MAX_FPS,
        "--video-codec", SCRCPY_VIDEO_CODEC,
        "--audio-codec", SCRCPY_AUDIO_CODEC,
        "--keyboard", SCRCPY_KEYBOARD,
        "--stay-awake",
        "--turn-screen-off",
    ]
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(MSG_SCRCPY_EXIT)
    else:
        print(MSG_SCRCPY_ERROR.format(result.returncode))
    return result.returncode


# ==================== 主程序 ====================

def main() -> None:
    _init_quit_handler()

    print("=" * 50)
    print(MSG_TITLE)
    print("=" * 50)

    # 步骤 1：ADB 连接设备
    run_adb_connect(DEVICE_ADDRESS)

    # 步骤 2：列出已连接设备，确认目标设备在线
    devices_output = run_adb_devices()
    if is_device_online(DEVICE_ADDRESS, devices_output):
        print(MSG_DEVICE_FOUND.format(DEVICE_ADDRESS))
    else:
        print(MSG_DEVICE_NOT_FOUND)

    # 步骤 3：启动 Scrcpy（阻塞直到用户关闭窗口）
    run_scrcpy(DEVICE_ADDRESS)


# ==================== 程序入口 ====================

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)
    except Exception as e:
        print(MSG_ERROR.format(e))
    finally:
        input(MSG_EXIT)
