# 请帮我写个中文的 Python 脚本，批注也是中文：
# 无线 Scrcpy 启动脚本：通过 ADB 连接本地或远程设备，然后启动 Scrcpy 投屏。
# 命令类似：scrcpy -s 100.64.0.3:41153 --video-bit-rate=2M --max-fps=30 --video-codec=h265 --audio-codec=opus --keyboard=uhid --mouse=sdk --stay-awake

# 导入模块
import sys
import subprocess

# ==================== 全局配置 ====================
WIRELESS_DEVICES = [
    "100.64.0.3:41153",
    "192.168.0.195:41153",
]

SCRCPY_VIDEO_BITRATE = "2M"
SCRCPY_MAX_FPS = "30"
SCRCPY_VIDEO_CODEC = "h265"
SCRCPY_AUDIO_CODEC = "opus"
SCRCPY_KEYBOARD = "uhid"
SCRCPY_MOUSE = "sdk"

# ==================== 消息 ====================
TITLE = "Scrcpy 启动工具"

# ==================== subprocess 通用函数 ====================
def run_command(cmd, timeout=15):
    """
    执行外部命令。
    统一使用 UTF-8，
    避免 Windows GBK 编码导致异常。
    """
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
# ==================== ADB ====================
def run_adb_devices():
    """
    获取 adb 设备列表。
    """
    print("正在检查已连接设备...")
    result = run_command(
        ["adb", "devices"],
        timeout=10,
    )
    stdout = result.stdout or ""
    stderr = result.stderr or ""
    if result.returncode != 0:
        raise RuntimeError(
            stderr.strip()
        )
    print(stdout.strip())
    return stdout
def adb_connect(address):
    """
    连接无线 ADB。
    """
    print(
        f"正在连接 ADB 设备：{address}"
    )
    result = run_command(
        [
            "adb",
            "connect",
            address,
        ],
        timeout=15,
    )
    stdout = (
        result.stdout or ""
    ).strip()
    stderr = (
        result.stderr or ""
    ).strip()
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
def get_usb_device(devices):
    """
    获取 USB ADB 设备。
    排除：
    IP:PORT 类型的无线设备。
    """
    for line in devices.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(
            "List of devices"
        ):
            continue
        parts = line.split()
        if len(parts) >= 2:
            serial = parts[0]
            state = parts[1]
            if (
                state == "device"
                and ":" not in serial
            ):
                return serial
    return None
def is_device_online(address, devices):
    """
    判断无线设备是否在线。
    """
    for line in devices.splitlines():
        if line.startswith(address):
            if "\tdevice" in line:
                return True
    return False
# ==================== 用户选择 ====================
def choose_mode():
    """
    选择连接模式。
    """
    print()
    print("请选择连接方式：")
    print()
    print("1. USB 本地连接（默认）")
    print("2. ADB 无线连接")
    print()
    while True:
        choice = input(
            "请输入 (1/2，直接回车默认1)："
        ).strip()
        if choice == "":
            return "usb"
        if choice == "1":
            return "usb"
        if choice == "2":
            return "wifi"
        print(
            "输入错误，请重新输入。"
        )
def choose_wireless_device():
    """
    选择无线设备。
    """
    print()
    print("请选择无线设备：")
    print()
    for index, device in enumerate(
        WIRELESS_DEVICES,
        start=1
    ):
        print(
            f"{index}. {device}"
        )
    print()
    while True:
        choice = input(
            "请输入编号（默认1）："
        ).strip()
        if choice == "":
            return WIRELESS_DEVICES[0]
        if choice.isdigit():
            index = int(choice) - 1
            if (
                0 <= index <
                len(WIRELESS_DEVICES)
            ):
                return WIRELESS_DEVICES[index]
        print(
            "输入错误，请重新输入。"
        )
# ==================== Scrcpy ====================
def run_scrcpy(serial):
    """
    启动 Scrcpy。
    """
    print(
        "正在启动 Scrcpy..."
    )
    cmd = [
        "scrcpy",
        "-s",
        serial,
        "--video-bit-rate",
        SCRCPY_VIDEO_BITRATE,
        "--max-fps",
        SCRCPY_MAX_FPS,
        "--video-codec",
        SCRCPY_VIDEO_CODEC,
        "--audio-codec",
        SCRCPY_AUDIO_CODEC,
        "--keyboard",
        SCRCPY_KEYBOARD,
        "--mouse",
        SCRCPY_MOUSE,
        "--stay-awake",
        "--turn-screen-off",
    ]
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(
            "Scrcpy 已退出。"
        )
    else:
        print(
            f"Scrcpy 返回码：{result.returncode}"
        )
# ==================== 主程序 ====================
def main():
    print("=" * 50)
    print(TITLE)
    print("=" * 50)
    mode = choose_mode()
    # ----------------------------
    # USB 本地连接
    # ----------------------------
    if mode == "usb":
        devices = run_adb_devices()
        serial = get_usb_device(
            devices
        )
        if serial is None:
            print(
                "未找到 USB ADB 设备。"
            )
            return
    # ----------------------------
    # 无线连接
    # ----------------------------
    else:
        address = choose_wireless_device()
        adb_connect(address)
        devices = run_adb_devices()
        if is_device_online(
            address,
            devices,
        ):
            print(
                f"设备已就绪：{address}"
            )
        else:
            print(
                "警告：设备未确认在线，继续尝试。"
            )
        serial = address
    print(
        f"使用设备：{serial}"
    )
    run_scrcpy(serial)
# ==================== 程序入口 ====================
if __name__ == "__main__":
    if hasattr(
        sys.stdout,
        "reconfigure"
    ):
        sys.stdout.reconfigure(
            encoding="utf-8",
            errors="replace",
        )
    try:
        main()
    except KeyboardInterrupt:
        print(
            "\n用户中断程序。"
        )
    except FileNotFoundError as e:
        print(
            f"\n找不到程序：{e.filename}"
        )
    except Exception as e:
        print(
            f"\n程序运行错误：{e}"
        )
    finally:
        try:
            input(
                "\n按回车键退出..."
            )
        except EOFError:
            pass