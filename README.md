# Sunway iCheckin 批量自动打卡工具

本项目用于自动批量登录 Sunway iZone 平台并完成打卡，适合需要为多个账号自动完成 iCheckin 操作的用户。

## 目录

* [环境要求](#环境要求)
* [快速开始](#快速开始)

  * [1. 安装 uv 包管理器](#1-安装-uv-包管理器)
  * [2. 安装依赖](#2-安装依赖)
  * [3. 配置用户文件 users.csv](#3-配置用户文件-userscsv)
  * [4. 可选：配置 ua.csv](#4-可选配置-uacsv)
  * [5. 运行脚本](#5-运行脚本)
* [users.csv 格式说明](#userscsv-格式说明)
* [ua.csv 格式说明](#uacsv-格式说明)
* [常见问题](#常见问题)
* [致谢](#致谢)

---

## 环境要求

* Python 3.8 及以上
* 推荐使用 [`uv`](https://docs.astral.sh/uv/getting-started/installation/) 进行依赖管理和运行（更快更简洁！）

---

## 快速开始

### 1. 安装 uv 包管理器

uv 是一个比 pip 更快、更干净的包管理工具。推荐用它来安装依赖和运行脚本。

**安装方法：**

* **适用于Windows系统**

  ```bash
  powershell -c "irm https://astral.sh/uv/install.ps1 | more"
  ```
* **适用于 macOS/Linux系统**

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | less
  ```
* 更多平台和方式，请查看官方文档：[uv 安装教程](https://docs.astral.sh/uv/getting-started/installation/)

---

### 2. 安装依赖

在项目根目录下执行：

```bash
uv sync
```

### 3. 配置用户文件 users.csv

在项目目录下，**新建或编辑 `users.csv` 文件**，用来填写需要打卡的所有用户账号和密码。

**格式如下：**

```csv
id,password
your_id_1,your_password_1
your_id_2,your_password_2
...
```

> ⚠️ 第一行为表头，**不要删除**。
> ⚠️ 一行一个账号，`id` 为学号，`password` 为密码。

**示例：**

```csv
id,password
24018567,abc12345
24019999,helloWorld
```

---

### 4. 可选：配置 ua.csv

`ua.csv` 用于自定义/批量设置 User-Agent，可提升安全性和模拟不同设备。
没有 `ua.csv` 时，脚本会用内置默认 UA。

**格式如下：**

```csv
user_agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15
...
```

> 第一行为表头。

---

### 5. 运行脚本

在命令行输入：

```bash
uv python main.py
```

或（如无 uv，可直接用 Python，但推荐用 uv）：

```bash
python main.py
```

运行后，脚本会提示输入一次打卡码（checkin code），**所有用户都会使用同一个 code 进行打卡**。

---

## users.csv 格式说明

* 必须在项目同级目录下
* UTF-8 编码保存
* 格式固定为：

  ```
  id,password
  你的学号,你的密码
  ...
  ```
* 示例：

  ```
  id,password
  24018566,abc12345
  24019999,helloWorld
  ```

---

## ua.csv 格式说明

* 可选文件
* 用于批量自定义 User-Agent
* 仅需填写 user\_agent 字段，每行一个 UA 字符串

示例内容：

```
user_agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...
```

---

## 常见问题

1. **为什么会提示用户登录失败？**

   * 请检查 `users.csv` 中账号密码是否正确
   * 注意密码不要用错字符或中文符号
2. **打卡失败或提示已打卡？**

   * 同一 code 多次打卡会提示“已打卡”
   * code 必须是当时有效的 iCheckin code （通常有效时间为 30 分钟）
3. **users.csv/ua.csv 打不开或出错？**

   * 确保文件是 UTF-8 编码，且表头与内容格式正确

---

## 致谢

感谢 [uv](https://docs.astral.sh/uv/) 团队和所有开源社区的支持。

shenming1115 ([GitHub 主页](https://github.com/shenming1115))

KevinTan2025 ([GitHub 主页](https://github.com/KevinTan2025))



如有任何问题，欢迎提 Issues 或留言！
