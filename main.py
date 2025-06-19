# coding:utf-8
# author:Wayne
# date:2025-06-19

import os
from dotenv import load_dotenv, find_dotenv

from GptranslateService import GPTTranslateService
from PlaceholderHtmlService import PlaceholderHtmlService


def get_system_prompt():
    """
    构造翻译提示词
    """
    return f"""
You are a senior translator and copy editor specialized in blockchain and cryptocurrency. Your task is to translate HTML content into the requested language and rewrite it to sound natural and native.

TASK  
1. Translate visible text in the HTML to the target language.  
2. Rewrite it to sound fluent, idiomatic, and culturally natural—as if originally written by a native speaker.

FORMATTING RULES  
- Do not add/remove/reorder any HTML tags or line breaks.  
- Keep all tag structures, including <br/>, <img/>, <input/>, unchanged.  
- Preserve all placeholders (e.g. {{ATTR_001}}, {{price}}, %s, :amount).  
- Translate attribute values like alt, title, and placeholder if present.  
- Output final HTML only, without comments or extra text.

QUALITY  
- Use native idioms and tone (formal/informal depending on source).  
- No omissions, additions, or meaning changes.  
- Maintain inline HTML entities (e.g. &nbsp;, &amp;).

CRYPTO-SPECIFIC  
- Use standard translations for blockchain terms: NFT, DeFi, DAO, Web3, etc.  
- Keep coin names (BTC, ETH, USDT) as-is unless local convention differs.  
- Translate financial terms like APY, gas fee using community-accepted wording.  
- Follow terminology from major exchanges in the target language.

FINAL NOTE  
Translate → Rewrite → Output full HTML with structure and placeholders untouched.
"""


def translate_html_file(input_file, output_file, translator_service, html_parse_service, prompt, origin_language,
                        target_language):
    """
    翻译单个HTML文件
    """
    print(f"\n=== 开始翻译 {input_file} ===")

    # 读取原始HTML文件
    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()

    print(f"原始HTML大小: {len(html):,} 字符")

    # 1. 使用占位符服务精简HTML
    compiled_html, attr_dict = html_parse_service.extract_html(html=html)
    print(f"精简后HTML大小: {len(compiled_html):,} 字符 ({len(compiled_html) / len(html) * 100:.1f}%)")
    print(f"提取属性数量: {len(attr_dict)}")

    # 2. 获取翻译结果
    print("正在翻译...")
    translated_content = translator_service.translate(html_text=compiled_html, prompt_content=prompt,
                                                      origin_language=origin_language, target_language=target_language)

    # 3. 恢复原来的样子，添加属性，图片地址，超链接等
    result_html = html_parse_service.restore_html(''.join(translated_content), attr_dict)
    print(f"最终HTML大小: {len(result_html):,} 字符")

    # 4. 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result_html)

    print(f"✅ 翻译完成，结果已保存到: {output_file}")
    return result_html


def test_single_file(file_name):
    """
    测试单个文件（用于调试）
    """
    print(f"=== 测试单个文件: {file_name} ===")

    # 加载环境变量
    load_dotenv(find_dotenv())
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("请先在环境变量中设置 OPENAI_API_KEY")

    # 初始化服务
    translator_service = GPTTranslateService(auth_key=api_key, max_len=30000)
    html_parse_service = PlaceholderHtmlService()

    # 构造翻译提示词
    system_prompt = get_system_prompt()

    # 文件路径
    test_htmls_dir = 'test_htmls'
    input_file = os.path.join(test_htmls_dir, f"{file_name}.html")
    output_file = os.path.join(test_htmls_dir, f"{file_name}.result.html")

    # 源文和目标语言
    origin_language = 'English'
    target_language = 'Traditional Chinese'

    if not os.path.exists(input_file):
        print(f"错误: 文件 {input_file} 不存在")
        return

    # 翻译文件
    translate_html_file(
        input_file=input_file,
        output_file=output_file,
        translator_service=translator_service,
        html_parse_service=html_parse_service,
        prompt=system_prompt,
        origin_language=origin_language,
        target_language=target_language
    )


if __name__ == '__main__':
    # 测试单个文件：
    test_single_file('origin3')
