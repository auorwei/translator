# HTML国际化翻译工具

基于GPT的HTML内容智能翻译工具，专注于区块链和加密货币领域的专业翻译。

## 功能特点

- 智能保持HTML结构完整性
- 专业术语（区块链、加密货币）准确翻译
- 支持大型HTML文件分块处理
- 自动保护HTML属性和占位符
- 支持多种GPT模型配置

## 安装

1. 克隆仓库：
```bash
git clone [repository-url]
cd html-translator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
创建 `.env` 文件并添加您的OpenAI API密钥：
```
OPENAI_API_KEY=your-api-key-here
```

## 使用方法

1. 准备HTML文件：
将需要翻译的HTML文件放在 `test_htmls` 目录下。

2. 运行翻译：
```python
python main.py
```

3. 查看结果：
翻译后的文件将保存在 `test_htmls` 目录下，文件名格式为 `[原文件名].result.html`。

## 配置说明

在 `main.py` 中可以配置：
- 源语言和目标语言
- GPT模型选择
- 最大文本长度
- 测试文件名

## 项目结构

```
api_translator/
├── GptranslateService.py    # GPT翻译服务
├── HtmlParseService.py      # HTML解析服务
├── PlaceholderHtmlService.py # HTML占位符处理
├── main.py                  # 主程序
└── test_htmls/             # 测试文件目录
```

## 注意事项

- 请确保您有足够的OpenAI API额度
- 大文件会被自动分块处理
- 翻译结果的质量取决于选择的GPT模型

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License 