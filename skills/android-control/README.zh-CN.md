# android-control

[English guide](README.md)

从当前宿主操作已识别的真实 Android 手机：检查界面与文件、管理应用、恢复连接，
并在设备上验证结果。这是手机操作 Skill，不是 Android 应用开发工具包。
它不依赖某种桌面、手机型号、应用清单或账户。

## 使用与依赖

将完整目录复制到智能体宿主支持的 Skill 位置。英文 `SKILL.md` 提供方法，
辅助脚本与操作参考随包保留。智能体需要实际可用的命令和设备访问能力，以及任务
已有的授权；本包不授予权限。

设备清单检查需要 Python 3.9+，以及位于 PATH 的 Android SDK Platform-Tools
（`adb`）。界面检查还需要同一 Python 环境中的
[uiautomator2](https://github.com/openatx/uiautomator2)。
可以使用虚拟环境；[uv](https://docs.astral.sh/uv/) 是可选替代。
手机侧调试与信任设置见[连接设置和操作示例](references/phone-environment.md)。
安装与界面动作使用接收方实际拥有的工具。

请求示例：“在已连接的手机上检查 Example App 的仅 Wi-Fi 更新开关，打开它，
重新进入页面，验证设置已保存。”智能体会检查连接别名、识别目标实体设备，
使用当前控件执行范围内的动作，并读回持久状态。

```bash
python3 scripts/android_inspect.py devices --timeout 20
uv run --no-project --with uiautomator2 python scripts/android_inspect.py ui --serial SERIAL --package com.example.app --timeout 20
python3 -m unittest discover -s scripts -p 'test_*.py'
```

脚本输出紧凑 JSON，仅执行只读检查。测试使用模拟对象，不需要设备、adb 或
uiautomator2。每条 ADB 请求分别限时；界面连接与层级读取共用一个限时子进程。
密码节点和常见令牌文本会被遮蔽，但输出仍可能包含设备标识、私人标签和未识别的
秘密，应保留在私有任务中。

## 包内容与调整

完整包包括英文方法、设置参考、辅助脚本、模拟测试、可选智能体元数据及含义一致
的中英文指南。公开版保留原本地 Skill 的设备识别、限定范围检查、读回验证、
临时设置恢复和隐私方法，将所有者特定的手机、应用和账户观察替换为通用设置与
操作示例，并加入界面检查限时。不包含私人设备记录或凭据。

本独立包采用 [MIT 许可](LICENSE)。上游依赖保留各自许可；本包不包含上游二进制文件。
