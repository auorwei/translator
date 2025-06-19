# coding:utf-8
# author:Wayne
# date:2025-06-19


from openai import OpenAI


class GPTTranslateService(object):
    def __init__(self, auth_key: str, max_len: int = 30000, model: str = 'gpt-4.1-nano'):
        self.max_len = max_len
        self.model = model
        # 创建客户端
        self.gpt_client = OpenAI(api_key=auth_key)

    def _chunk_html(self, html_text: str):
        parts = html_text.split(">")
        chunks, buffer = [], ""
        for part in parts:
            fragment = part + ">"
            if len(buffer) + len(fragment) > self.max_len:
                chunks.append(buffer)
                buffer = fragment
            else:
                buffer += fragment
        if buffer:
            chunks.append(buffer)
        return chunks

    def translate(self, html_text: str, prompt_content: str, origin_language: str, target_language):

        # 1. Chunk
        chunks = self._chunk_html(html_text)

        # 2. Translate each chunk
        translated_chunks = []
        for chunk in chunks:
            messages = [
                {"role": "system", "content": prompt_content},
                {"role": "user", "content": f"translate this html from {origin_language} to {target_language}:{chunk}"}
            ]

            response = self.gpt_client.chat.completions.create(
                model=self.model,  # 或者 "gpt-4", "gpt-3.5-turbo" 等可用模型
                messages=messages,
                temperature=0.7,  # 可选：控制生成文本的随机性
                max_tokens=self.max_len  # 可选：限制回复长度
            )

            content = response.choices[0].message.content
            translated_chunks.append(content)
        return translated_chunks
