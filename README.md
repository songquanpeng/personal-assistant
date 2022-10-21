# 个人助理应用
> 让生活简单一点的个人助理应用


<p>
  <a href="https://raw.githubusercontent.com/songquanpeng/personal-assistant/main/LICENSE">
    <img src="https://img.shields.io/github/license/songquanpeng/personal-assistant?color=brightgreen" alt="license">
  </a>
  <a href="https://github.com/songquanpeng/personal-assistant/releases/latest">
    <img src="https://img.shields.io/github/v/release/songquanpeng/personal-assistant?color=brightgreen&include_prereleases" alt="release">
  </a>
  <a href="https://github.com/songquanpeng/personal-assistant/releases/latest">
    <img src="https://img.shields.io/github/downloads/songquanpeng/personal-assistant/total?color=brightgreen&include_prereleases" alt="release">
  </a>
</p>

可在 [Release 页面](https://github.com/songquanpeng/personal-assistant/releases)下载最新版本（Windows，macOS，Linux）。

## 功能
1. 休息提醒，包含多种提醒方式。
2. 定时任务，定时执行各种命令。
   1. 内置命令 `@tray` 可用于定时发送系统消息。
   2. 内置命令 `@msg` 可用于定时通过 [Message Pusher](https://github.com/songquanpeng/message-pusher) 发送消息（需要在`其他设置`页面配置好 Message Pusher 的服务地址和 token）。
3. 周期待办，自动添加待办事项。

## 截图展示
![demo](demo.png)

## 使用方法
### Windows 用户  
直接双击 personal-assistant.exe 运行。

### macOS 用户
1. 给执行权限：`chmod u+x personal-assistant-macos`；
2. 之后直接双击运行 personal-assistant-macos 或在终端中运行都可。

### Linux 用户
同上，区别在于文件名换成 `personal-assistant`。

## 打包流程
```bash
pip install -r requirements.txt
pyuic5 -o ui.py main.ui
pyrcc5 -o resource_rc.py resource.qrc 
pyinstaller --noconsole -F ./main.py --icon icon.png -n personal-assistant.exe
```
