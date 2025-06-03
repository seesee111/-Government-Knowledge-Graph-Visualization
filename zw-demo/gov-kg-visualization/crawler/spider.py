import requests
import json

class GovernmentCrawler:
    def __init__(self):
        # 用于存储抓取到的数据
        self.data = []

    def fetch_api(self, page=1, page_size=15):
        """
        抓取指定页码的政务事项数据
        :param page: 页码
        :param page_size: 每页条数
        :return: 返回接口返回的JSON数据
        """
        url = "https://www.lnzwfw.gov.cn/matter/catalogInf/findCatalog"
        params = {
            "pageNum": page,
            "pageSize": page_size
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        # 发送GET请求
        response = requests.get(url, params=params, headers=headers, proxies={"http": None, "https": None})
        print(f"Page {page} status: {response.status_code}")
        print(response.text[:500])  # 打印前500字符，便于调试
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch page {page}, status: {response.status_code}")
            return None

    def run(self, max_pages=10):
        """
        循环抓取多页数据
        :param max_pages: 最大抓取页数
        """
        for page in range(1, max_pages + 1):
            result = self.fetch_api(page)
            print(result)  # 调试用，打印返回内容
            # 判断返回数据结构是否正确
            if not result or "faqList" not in result or "list" not in result["faqList"]:
                break
            items = result["faqList"]["list"]
            if not items:
                break
            # 提取每条事项的关键信息
            for item in items:
                self.data.append({
                    "授权部门": item.get("businesscodes", ""),
                    "职权编码": item.get("catalogCode", ""),
                    "事项名称": item.get("qlName", ""),
                    "事项类型": item.get("qlKind", ""),
                    "依据": item.get("lawbasis", ""),
                    "实施层级": item.get("shiquancj", "")
                })

    def save_data(self, filename='government_data.json'):
        """
        将抓取到的数据保存为JSON文件
        :param filename: 文件名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    crawler = GovernmentCrawler()
    crawler.run(max_pages=2)  # 先试2页，调试用
    crawler.save_data()