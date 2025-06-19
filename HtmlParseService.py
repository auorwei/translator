# coding:utf-8
# author:Wayne
# date:2025-06-19

import re


class HtmlParseServices(object):

    @staticmethod
    def decompose(html: str):
        """
        拆解：移除所有属性，返回简化后的 HTML 和
        [(slash, tag, attrs, self_closing), …] 列表
        """
        tokens = re.split(r'(<[^>]+>)', html)
        attr_list = []
        stripped = []
        tag_re = re.compile(r'<\s*(/?)([^\s/>]+)([^>]*)>')

        for t in tokens:
            m = tag_re.match(t)
            if m:
                slash, tag, rest = m.groups()
                raw = rest.strip()
                self_closing = raw.endswith('/')
                if self_closing:
                    raw = raw[:-1].strip()
                # 存下原始属性和自闭合信息
                attr_list.append((slash, tag, raw, self_closing))
                # 生成无属性标签
                stripped.append(f'<{slash}{tag}{" /" if self_closing else ""}>')
            else:
                stripped.append(t)

        return ''.join(stripped), attr_list

    @staticmethod
    def recompose(translated_html: str, attr_list):
        """
        重组：只对“和原始标签名匹配”的标签插入属性，
        对翻译时新增的标签原样保留，不抛错。
        """
        tokens = re.split(r'(<[^>]+>)', translated_html)
        recomposed = []
        idx = 0
        tag_re = re.compile(r'<\s*(/?)([^\s/>]+)([^>]*)>')

        for t in tokens:
            m = tag_re.match(t)
            if m and idx < len(attr_list):
                slash, tag, _ = m.groups()
                orig_slash, orig_tag, attrs, self_closing = attr_list[idx]
                # 只有标签名和闭合类型都“对得上号”才插属性
                if slash == orig_slash and tag == orig_tag:
                    if attrs:
                        # 恢复成 <tag attrs> 或 <tag attrs/>
                        tail = '/' if self_closing else ''
                        recomposed.append(f'<{slash}{tag} {attrs}{tail}>')
                    else:
                        tail = '/' if self_closing else ''
                        recomposed.append(f'<{slash}{tag}{tail}>')
                    idx += 1
                else:
                    # 这可能是翻译引擎新增/修改的标签，原样保留
                    recomposed.append(t)
            else:
                # 普通文本或已耗尽 attr_list
                recomposed.append(t)

        return ''.join(recomposed)
