# UV 包管理器功能体验实验计划

本项目旨在全面体验 UV 包管理器（一个由 Rust 编写的高性能 Python 包管理工具）的各项功能。通过以下实验，您可以深入了解 UV 相比传统 Python 包管理工具的优势。

## 实验一：安装与基础配置

1. **安装 uv**
   ```bash
   # Linux/macOS
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   ```powershell
   # Windows
   winget install --id=astral-sh.uv -e
   # 或使用
   irm 'https://astral.sh/uv/install.ps1' -UseBasicParsing | iex
   ```

2. **验证安装**
   ```bash
   # 所有系统
   uv --version
   ```

## 实验二：项目初始化与虚拟环境管理

1. **初始化项目**（如果已在项目目录中）
   ```bash
   # 所有系统
   uv init
   ```

2. **查看项目结构**
   ```bash
   # Linux/macOS
   ls -la
   cat pyproject.toml
   ```
   ```powershell
   # Windows
   Get-ChildItem
   Get-Content pyproject.toml
   ```

3. **检查虚拟环境**
   ```bash
   # Linux/macOS
   ls -la .venv
   ```
   ```powershell
   # Windows
   Get-ChildItem .venv
   ```

## 实验三：依赖管理基础

1. **添加基本依赖**
   ```bash
   # 所有系统
   uv add requests flask
   ```

2. **查看更新后的 pyproject.toml**
   ```bash
   # Linux/macOS
   cat pyproject.toml
   ```
   ```powershell
   # Windows
   Get-Content pyproject.toml
   ```

3. **查看生成的锁定文件**
   ```bash
   # Linux/macOS
   cat uv.lock
   ```
   ```powershell
   # Windows
   Get-Content uv.lock
   ```

4. **运行测试应用**
   ```bash
   # 所有系统
   uv run python app.py
   ```

5. **在浏览器访问**
   ```
   http://127.0.0.1:5000/
   http://127.0.0.1:5000/get
   ```

## 实验四：依赖解析与冲突处理

1. **添加特定版本依赖**
   ```bash
   # 所有系统
   uv add "numpy<2.0.0"
   ```

2. **尝试添加冲突版本**
   ```bash
   # 所有系统
   uv add "pandas>=2.0.0"  # 这可能导致依赖冲突
   ```

3. **查看冲突信息并解决**
   ```bash
   # 所有系统
   uv add "pandas<2.0.0"  # 使用兼容版本
   ```

## 实验五：可选依赖与依赖组

1. **添加可选依赖**
   ```bash
   # 所有系统
   uv add pytest --optional test
   uv add black flake8 --optional lint
   ```

2. **查看更新后的 pyproject.toml**
   ```bash
   # Linux/macOS
   cat pyproject.toml
   ```
   ```powershell
   # Windows
   Get-Content pyproject.toml
   ```

3. **创建测试文件**
   ```bash
   # 所有系统
   uv sync --extra test
   ```

4. **运行测试**
   ```bash
   # 所有系统
   uv run pytest test_example.py
   ```

5. **添加依赖组**
   ```bash
   # 所有系统
   uv add sphinx --group docs
   ```

6. **从特定组安装依赖**
   ```bash
   # 所有系统
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
   ```bash
   # 所有系统
   uv add torch torchvision
   ```

3. **测试安装**
   ```bash
   # 所有系统
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
   ```bash
   # 所有系统
   uv sync
   ```

## 实验八：性能对比测试

1. **创建一个复杂依赖测试**
   ```bash
   # Linux/macOS
   mkdir perf_test
   cd perf_test
   ```
   ```powershell
   # Windows
   New-Item -ItemType Directory -Name perf_test
   Set-Location perf_test
   ```

2. **创建 requirements.txt**
   ```bash
   # Linux/macOS
   echo "django\ncelery\npytest\nsphinx\nmatplotlib\nscikit-learn\nsqlalchemy\nblack\nflake8" > requirements.txt
   ```
   ```powershell
   # Windows
   "django`ncelery`npytest`nsphinx`nmatplotlib`nscikit-learn`nsqlalchemy`nblack`nflake8" | Out-File -FilePath requirements.txt
   ```

3. **使用 pip 安装并计时**
   ```bash
   # Linux/macOS
   python -m venv pip_env
   time pip_env/bin/pip install -r requirements.txt
   ```
   ```powershell
   # Windows
   python -m venv pip_env
   Measure-Command { pip_env\Scripts\pip install -r requirements.txt }
   ```

4. **使用 uv 安装并计时**
   ```bash
   # Linux/macOS
   time uv pip install -r requirements.txt
   ```
   ```powershell
   # Windows
   Measure-Command { uv pip install -r requirements.txt }
   ```

5. **比较二者时间差异**

## 实验九：Python 版本管理

1. **指定 Python 版本创建环境**
   ```bash
   # 所有系统
   uv venv --python 3.9
   ```

2. **查看环境信息**
   ```bash
   # 所有系统
   uv run python --version
   ```

## 实验十：全局工具安装

1. **安装常用开发工具**
   ```bash
   # 所有系统
   uv install black
   uv install httpie
   ```

2. **测试安装的工具**
   ```bash
   # 所有系统
   black --version
   http --version
   ```

## 总结分析

完成以上实验后，对比 UV 与传统工具（如 pip、conda）在以下方面的差异：

1. 安装速度
2. 依赖解析效率
3. 环境管理集成度
4. 使用便捷性
5. 冲突处理能力

记录实验结果并分析 UV 的优缺点以及适用场景。 