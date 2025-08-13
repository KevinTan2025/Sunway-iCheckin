# Sunway iCheckin Auto Check-in Tool

This project is designed to automatically log in to the Sunway iZone platform in batches and complete iCheckin for multiple accounts. It is ideal for users who need to automate iCheckin for several accounts.

[🌟 English](README.md) | [🌏 中文](README-CN.md)

## ⚠️ **DISCLAIMER / 免责声明**

**ENGLISH:**
This software is provided "AS IS" without warranty of any kind. The authors and contributors of this project are not responsible for any consequences, damages, or issues that may arise from using this software. Users assume full responsibility for their use of this software and any resulting outcomes. Use at your own risk.

**中文:**
本软件按"现状"提供，不提供任何形式的保证。本项目的作者和贡献者不对使用本软件可能产生的任何后果、损害或问题承担责任。用户对使用本软件及其产生的任何结果承担全部责任。使用风险自负。

## Table of Contents

* [Download & Installation](#download--installation)
* [Quick Start (For Developers)](#quick-start-for-developers)
  * [1. Install uv Package Manager](#1-install-uv-package-manager)
  * [2. Install Dependencies](#2-install-dependencies)
  * [3. Configure users.csv](#3-configure-userscsv)
  * [4. (Optional) Configure ua.csv](#4-optional-configure-uacsv)
  * [5. Run the Script](#5-run-the-script)
* [users.csv Format](#userscsv-format)
* [ua.csv Format](#uacsv-format)
* [FAQ](#faq)
* [Acknowledgements](#acknowledgements)

---

## Download & Installation

**For regular users (Recommended):**

1. Go to the [Releases](https://github.com/KevinTan2025/Sunway/releases) page
2. Download the latest version (v1.0.0) of `Sunway iCheckIn.exe`
3. Run the executable directly - no Python installation or environment setup required!

The executable includes everything you need and will create necessary files (like `users.json`) in the same directory.

---

## Quick Start (For Developers)

**Note:** If you downloaded the executable from Releases, you can skip this section.

**Requirements for development:**
* Python 3.8 or higher
* It is recommended to use [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for dependency management and running the script (it's faster and easier!)

### 1. Install uv Package Manager

uv is a faster and cleaner package management tool compared to pip. It's recommended for installing dependencies and running scripts.

**Installation:**

* **For Windows:**

  ```bash
  powershell -c "irm https://astral.sh/uv/install.ps1 | more"
  ```
* **For macOS/Linux:**

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | less
  ```
* For more platforms and methods, check the official docs: [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)

---

### 2. Install Dependencies

In the project root directory, run:

```bash
uv sync
```

### 3. Configure users.csv

Create or edit the `users.csv` file in your project directory. This file should include all the user IDs and passwords for the accounts you want to check in.

**Format:**

```csv
id,password
your_id_1,your_password_1
your_id_2,your_password_2
...
```

> ⚠️ The first line is the header. **Do not remove it.**
> ⚠️ One account per line. `id` is the student ID, `password` is the password.

**Example:**

```csv
id,password
24018567,abc12345
24019999,helloWorld
```

---

### 4. (Optional) Configure ua.csv

The script already includes a small set of common User-Agents. If you want to supply your own list, create a `ua.csv` file in the same folder. When present, the file overrides the built-in list.

**Format:**

```csv
user_agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15
...
```

> The first line is the header.

---

### 5. Run the Script

Run the following command in your terminal:

```bash
uv python main.py
```

Or (if you don't have uv, you can use Python directly, but uv is recommended):

```bash
python main.py
```

When running, the script will prompt you to enter the check-in code (iCheckin code). **All users will use the same code for check-in.**

---

## users.csv Format

* Must be in the project root directory
* Save as UTF-8 encoding
* Fixed format:

  ```
  id,password
  your_student_id,your_password
  ...
  ```
* Example:

  ```
  id,password
  24018566,abc12345
  24019999,helloWorld
  ```

---

## ua.csv Format

* Optional file
* Overrides the internal User-Agent list
* Only need to fill in the `user_agent` field, one UA string per line

Example content:

```
user_agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...
```

---

## FAQ

1. **Why does it say login failed for a user?**

   * Please check if the IDs and passwords in `users.csv` are correct
   * Be careful not to use wrong characters or Chinese symbols in the password
2. **Check-in failed or shows already checked in?**

   * Using the same code multiple times will result in an "already checked in" message
   * The code must be a valid and currently active iCheckin code (usually valid for 30 minutes)
3. **Can't open or error with users.csv/ua.csv?**

   * Make sure the file is UTF-8 encoded and the header and content format are correct

4. **Where is users.json saved when using the packaged executable?**

   * When running the GUI or a PyInstaller-built `.exe`, the `users.json` file will be created in the same directory as the executable. Ensure that directory is writable so your user list can be saved.

---

## Acknowledgements

Thanks to the [uv](https://docs.astral.sh/uv/) team and all open-source contributors for their support.

shenming1115 ([GitHub Profile](https://github.com/shenming1115))

KevinTan2025 ([GitHub Profile](https://github.com/KevinTan2025))

If you have any questions, feel free to open an Issue or leave a message!
