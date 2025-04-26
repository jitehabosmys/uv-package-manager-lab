# UV 包管理器功能体验实验

## 项目简介

本项目旨在全面体验 UV 包管理器（一个由 Rust 编写的高性能 Python 包管理工具）的各项功能。通过以下实验，您可以深入了解 UV 相比传统 Python 包管理工具的优势。

## 环境要求

- Windows 操作系统
- Python 3.8+ 安装
- 管理员权限（用于全局工具安装）

## 实验一：安装与基础配置

1. **安装 uv**
   ```powershell
   winget install --id=astral-sh.uv -e
   # 或使用
   irm 'https://astral.sh/uv/install.ps1' -UseBasicParsing | iex
   ```

2. **验证安装**
   ```powershell
   uv --version
   ```

## 实验二：项目初始化与虚拟环境管理

1. **初始化项目**（如果已在项目目录中）
   ```powershell
   uv init
   ```

2. **查看项目结构**
   ```powershell
   Get-ChildItem
   Get-Content pyproject.toml
   ```

3. **检查虚拟环境**
   ```powershell
   Get-ChildItem .venv
   ```

## 实验三：依赖管理基础

1. **添加基本依赖**
   ```powershell
   uv add requests flask
   ```

2. **查看更新后的 pyproject.toml**
   ```powershell
   Get-Content pyproject.toml
   ```

3. **查看生成的锁定文件**
   ```powershell
   Get-Content uv.lock
   ```

4. **运行测试应用**
   ```powershell
   uv run python app.py
   ```

5. **在浏览器访问**
   ```
   http://127.0.0.1:5000/
   http://127.0.0.1:5000/get
   ```

## 实验四：依赖解析与冲突处理

1. **添加第一个限制版本依赖**
   ```powershell
   uv add "numpy==1.22.0"
   ```

2. **尝试添加冲突版本**
   ```powershell
   uv add "pandas==1.3.5"  # 这会导致依赖冲突，因为 pandas 1.3.5 需要 numpy<1.22.0
   ```
   预期输出类似：
   ```
   error: No solution found when resolving dependencies:
   ╰─▶ Because pandas==1.3.5 depends on numpy>=1.20.0,<1.22.0 and you require numpy==1.22.0, we can conclude that pandas==1.3.5 is not compatible with your project.
   ```

3. **查看冲突信息并解决**
   ```powershell
   uv add "pandas==1.4.0"  # 使用兼容 numpy 1.22.0 的 pandas 版本
   ```

4. **也可以尝试直接安装两个冲突的同名包版本**
   ```powershell
   uv add "django==3.2.0"
   uv add "django==4.2.0"  # 这会导致直接冲突，尝试安装同一个包的两个不同版本
   ```

## 实验五：可选依赖与依赖组

1. **添加可选依赖**
   ```powershell
   uv add pytest --optional test
   uv add black flake8 --optional lint
   ```

2. **查看更新后的 pyproject.toml**
   ```powershell
   Get-Content pyproject.toml
   ```

3. **创建测试文件**
   ```powershell
   uv sync --extra test # 环境会被同步为只包含主要依赖和指定的可选依赖组
   ```

4. **运行测试**
   ```powershell
   uv run pytest test_example.py
   ```

5. **添加依赖组**
   ```powershell
   uv add sphinx --group docs # 开发依赖，发布时不会被包含在元数据中
   ```

6. **从特定组安装依赖**
   ```powershell
   uv sync --group docs
   ```

## 实验六：自定义索引源

1. **编辑 pyproject.toml，添加 PyTorch 索引**
   
   请使用文本编辑器添加以下内容到 pyproject.toml：
   ```toml
   [[tool.uv.index]]
   name = "pytorch-cpu"
   url = "https://download.pytorch.org/whl/cpu"
   explicit = true   
   
   [tool.uv.sources]
   torch = { index = "pytorch-cpu" }
   ```

2. **安装 PyTorch**
   ```powershell
   uv add torch torchvision
   ```

3. **测试安装**
   ```powershell
   uv run python -c "import torch; print(torch.__version__)"
   ```

## 实验七：环境标记与条件依赖

1. **编辑 pyproject.toml，添加基于环境的依赖**
   
   请使用文本编辑器添加以下内容到 pyproject.toml：
   ```toml
   [tool.uv.sources]
   torch = [
     { index = "pytorch-cpu", marker = "platform_system == 'Windows'" },
     { index = "pytorch-cpu", marker = "platform_system == 'Darwin'" },
     { index = "pytorch-cu124", marker = "platform_system == 'Linux'" },
   ]
   
   [[tool.uv.index]]
   name = "pytorch-cu124"
   url = "https://download.pytorch.org/whl/cu124"
   explicit = true
   ```

2. **更新环境**
   ```powershell
   uv sync
   ```

## 实验八：性能对比测试 (基于Windows平台)

1. **创建一个单独的测试目录**
   ```powershell
   # 在用户文档目录创建一个全新的测试文件夹（与当前项目完全隔离）
   $testDir = Join-Path $env:USERPROFILE "Documents\uv_perf_test"
   New-Item -ItemType Directory -Path $testDir -Force
   Set-Location $testDir
   ```

2. **创建 requirements.txt**
   ```powershell
   "django`ncelery`npytest`nsphinx`nmatplotlib`nscikit-learn`nsqlalchemy`nblack`nflake8" | Out-File -FilePath requirements.txt
   ```

3. **重置测试环境**
   ```powershell
   # 清除各工具的缓存
   Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\pip\Cache"
   Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\uv\Cache"
   conda clean --all -y
   
   # 删除之前的测试环境（如果存在）
   Remove-Item -Recurse -Force -ErrorAction SilentlyContinue pip_test_env
   Remove-Item -Recurse -Force -ErrorAction SilentlyContinue uv_test_env
   conda env remove -n conda_test_env -y -q 2>$null
   ```

4. **使用 pip 安装并计时（包含环境创建时间）**
   ```powershell
   # 测量创建环境和安装包的总时间
   Measure-Command {
      # 创建虚拟环境并安装包
      python -m venv pip_test_env
      pip_test_env\Scripts\python.exe -m pip install -r requirements.txt
   }
   ```

5. **使用 uv 安装并计时（包含环境创建时间）**
   ```powershell
   # 清除上一步可能产生的缓存
   Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\pip\Cache"
   Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\uv\Cache"
   
   # 测量创建环境和安装包的总时间
   Measure-Command {
      # 创建虚拟环境并安装包到该环境
      uv venv uv_test_env
      # 使用虚拟环境中的pip安装包
      uv pip install -r requirements.txt --python uv_test_env\Scripts\python.exe
   }
   ```

6. **使用 conda 安装并计时（包含环境创建时间）**
   ```powershell
   # 清除上一步可能产生的缓存
   Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\pip\Cache"
   Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\uv\Cache"
   conda clean --all -y
   
   # 测量创建环境和安装包的总时间
   Measure-Command {
      # 创建conda环境并安装pip
      conda create -n conda_test_env python pip -y
      # 使用该环境中的pip安装包
      conda run -n conda_test_env pip install -r requirements.txt
   }
   ```

7. **清理测试环境**
   ```powershell
   # 返回原始项目目录
   ```

8. **比较三者时间差异**
   - **实际测试结果**:
     ```
     # pip 总时间（环境创建+安装，无缓存）
     TotalSeconds: 69.2083774
     
     # uv 总时间（环境创建+安装，无缓存）
     TotalSeconds: 17.2576308
     
     # conda 总时间（环境创建+安装，无缓存）
     TotalSeconds: 91.9790123
     
     # 速度对比
     uv vs pip: 约 4.01 倍 (69.21/17.26)
     uv vs conda: 约 5.33 倍 (91.98/17.26)
     ```
   
   - **测试说明**:
     - 为确保测试公平性和避免干扰现有环境:
       1. 在完全独立的目录中进行测试
       2. 每种工具使用不同的目录和命名方式，避免混淆
       3. 测试包含虚拟环境创建和包安装的总时间
     - 所有测试都使用相同的 requirements.txt 文件
     - 记录的是完全冷启动（无缓存）情况下的性能表现
     - 这些测试在Windows平台上进行
   
   - **分析**:
     - UV 在创建环境和安装相同依赖时速度显著快于传统 pip (约4倍) 和 conda (约5倍)
     - UV 安装了67个包仅用了17秒，而pip需要69秒，conda需要92秒
     - UV 提供了更详细的安装进度和依赖解析信息
     - UV 并行下载和安装多个包，而pip更多是串行处理
     - UV 的依赖解析速度快(1.50秒)，准备包也非常迅速(5.87秒)
     - conda虽然在非Python依赖管理上有优势，但纯Python包安装性能明显弱于UV
     - 在日常Python开发中，UV可以显著提升包管理效率，节省开发时间

## 实验九：Python 版本管理

1. **指定 Python 版本创建环境**
   ```powershell
   uv venv --python 3.9
   ```

2. **查看环境信息**
   ```powershell
   uv run python --version
   ```

## 实验十：查看包依赖关系

```powershell
# 创建一个包含热门包的列表
"django`ntensorflow`npandas`nnumpy`nrequests" | Out-File -FilePath popular_packages.txt

# 查看这些热门包的完整依赖
uv pip compile popular_packages.txt -o popular_requirements.txt
```

## 总结分析

完成以上实验后，对比 UV 与传统工具（如 pip、conda）在以下方面的差异：

1. 安装速度：UV显著快于pip和conda
2. 依赖解析效率：UV的依赖解析更快速、准确
3. 环境管理集成度：提供完整的项目管理功能
4. 使用便捷性：命令简单直观，工作流程清晰
5. 冲突处理能力：提供清晰的冲突报告和解决建议

UV作为新一代Python包管理工具，在性能和用户体验上都有明显优势，特别适合需要快速环境配置、大型项目依赖管理的场景。

## 贡献

欢迎提交问题和改进建议！

## 许可

MIT

## 致谢

感谢[Astral](https://astral.sh)团队开发了这个出色的UV工具。

感谢[Cursor](https://cursor.sh)团队开发的智能编辑器，本项目主要基于Cursor进行开发。