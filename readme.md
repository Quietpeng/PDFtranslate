# PDF Translator (PDF文档翻译工具)

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)

一个功能强大的 PDF 文档翻译工具，支持批量翻译和单文件翻译，提供命令行和图形界面两种使用方式。基于 Google 翻译服务，支持多种语言互译。

## ✨ 功能特性

- 🚀 支持批量翻译整个文件夹下的 PDF 文件
- 📄 支持单个 PDF 文件翻译
- 🌍 支持多种语言互译（默认英译中）
- 💻 提供命令行和图形界面两种使用方式
- 📊 详细的翻译进度和状态显示
- 🔄 自动检测和配置代理
- 📁 自定义输入输出路径

## 🛠️ 安装说明

### 环境要求

- Python 3.6 或更高版本
- 稳定的网络连接（需要访问翻译服务）
- 可选：代理服务（如遇网络问题）

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/Quietpeng/PDFtranslate.git
cd pdf-translator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 📖 使用说明

### 图形界面模式

直接运行程序将启动图形界面：
```bash
python pdf_translator.py
```

图形界面功能：
- 选择源语言和目标语言
- 支持文件/文件夹选择对话框
- 实时显示翻译进度和状态
- 可随时查看翻译日志

### 命令行模式

```bash
python pdf_translator.py [-h] [-i INPUT] [-o OUTPUT] [-s SINGLE]

参数说明:
  -h, --help            显示帮助信息
  -i INPUT, --input INPUT
                        输入文件夹路径，用于批量翻译
  -o OUTPUT, --output OUTPUT
                        输出文件夹路径（可选，默认为'./翻译后output'）
  -s SINGLE, --single SINGLE
                        单个PDF文件路径，用于单文件翻译
```

### 使用示例

1. 翻译单个PDF文件：
```bash
python pdf_translator.py -s ./example.pdf -o ./output
```

2. 翻译整个文件夹：
```bash
python pdf_translator.py -i ./pdf_files -o ./translated_files
```

3. 使用默认输出路径：
```bash
python pdf_translator.py -i ./pdf_files
```

## ⚙️ 配置说明

### 支持的语言
- 中文 (zh)
- 英语 (en)
- 日语 (ja)
- 韩语 (ko)
- 法语 (fr)
- 德语 (de)
- 俄语 (ru)

### 代理设置
程序会自动尝试以下代理端口：
- 7890 (默认)
- 1080
- 8080

## 📝 注意事项

1. 首次运行时会自动下载必要的模型文件
2. 翻译大文件时可能需要较长时间，请耐心等待
3. 建议在翻译前备份原始文件
4. 如遇网络问题，请检查代理设置
5. 确保有足够的磁盘空间存储翻译后的文件

## 🔍 故障排除

1. 网络连接问题
   - 检查网络连接是否正常
   - 确认代理服务是否正常运行
   - 尝试使用不同的代理端口

2. 文件处理问题
   - 确保文件格式为PDF
   - 检查文件是否损坏
   - 确认有足够的磁盘空间

3. 翻译失败
   - 查看错误日志获取详细信息
   - 确保文件内容可以被正确识别
   - 尝试重新运行程序

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 🙏 致谢

- [PDFMathTranslate](https://github.com/Byaidu/PDFMathTranslate) - PDF翻译核心库
- 感谢所有开源项目的贡献者

## 👤 作者

**[@Quietpeng](https://github.com/Quietpeng)**

## 📄 更新日志

### v1.0.0 (2024-01)
- 初始版本发布
- 支持GUI和命令行两种使用方式
- 添加详细的翻译进度显示
- 支持多种语言互译
- 自动代理配置功能

---

如果这个项目对你有帮助，请给个 Star ⭐️！

