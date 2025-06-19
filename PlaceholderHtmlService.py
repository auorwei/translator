# coding:utf-8
# author:Wayne
# date:2025-06-19

import re
from typing import Tuple, Dict


class PlaceholderHtmlService:
    """
    占位符HTML处理服务
    核心思路：
    1. 提取所有标签属性，用占位符替换
    2. GPT只翻译包含占位符的纯文本
    3. 翻译后恢复原始属性
    """
    
    def __init__(self):
        self.attr_dict = {}  # 保存属性字典：{"ATTR_001": "src='...' alt='...'"}
        self.counter = 0     # 占位符计数器
    
    def extract_html(self, html: str) -> Tuple[str, Dict[str, str]]:
        """
        提取HTML中的属性，替换为占位符
        
        Args:
            html: 原始HTML字符串
            
        Returns:
            tuple: (处理后的HTML, 属性字典)
        """
        # 重置状态
        self.attr_dict = {}
        self.counter = 0
        
        # 检查是否存在占位符冲突
        if "{{ATTR_" in html:
            print("警告: 原HTML中包含占位符格式，可能会冲突")
        
        # 匹配开标签：<tagname attributes> 或 <tagname attributes/>
        # 允许标签名和属性之间有空格，支持多行属性
        pattern = r'<(\w+)(\s+[^>]*?)(\s*/)?>'
        
        def replace_attributes(match):
            tag_name = match.group(1)
            attributes = match.group(2) if match.group(2) else ""
            self_closing = match.group(3) if match.group(3) else ""
            
            # 如果没有属性（只有空格或无），直接返回原标签
            if not attributes or attributes.isspace():
                return match.group(0)
            
            # 清理属性字符串
            attributes = attributes.strip()
            if not attributes:
                return match.group(0)
            
            # 生成占位符
            self.counter += 1
            placeholder = f"ATTR_{self.counter:03d}"
            
            # 保存属性
            self.attr_dict[placeholder] = attributes
            
            # 返回带占位符的标签
            return f'<{tag_name} {{{{{placeholder}}}}}{self_closing}>'
        
        # 执行替换
        processed_html = re.sub(pattern, replace_attributes, html, flags=re.MULTILINE | re.DOTALL)
        
        return processed_html, self.attr_dict.copy()
    
    def restore_html(self, translated_html: str, attr_dict: Dict[str, str]) -> str:
        """
        恢复HTML中的属性
        
        Args:
            translated_html: 翻译后包含占位符的HTML
            attr_dict: 属性字典
            
        Returns:
            str: 恢复属性后的HTML
        """
        result_html = translated_html
        
        # 统计占位符使用情况
        placeholders_found = re.findall(r'\{\{(ATTR_\d+)\}\}', result_html)
        
        
        # 恢复每个占位符
        for placeholder in placeholders_found:
            if placeholder in attr_dict:
                # 替换占位符为原始属性
                placeholder_pattern = f'{{{{{placeholder}}}}}'
                result_html = result_html.replace(placeholder_pattern, attr_dict[placeholder])
            else:
                print(f"警告: 未找到占位符 {placeholder} 对应的属性")
        
        return result_html

