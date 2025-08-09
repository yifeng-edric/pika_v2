import re


class ParseUtils:
    @staticmethod
    def extract_markdown_links(text):
        pattern = r"!\[.*?\]\((.*?)\)"
        links = re.findall(pattern, text)
        return links

    @staticmethod
    def extract_wx_business_card(text):
        pattern = r"##{(.*?)}"
        links = re.findall(pattern, text)
        return links
