# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class TiebaPipeline:
    def open_spider(self, spider):
        self.file = open(r'E:\python_test\scrapytest\tieba\xiaohua.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item) 
        # It provides a common interface to extract and set data without having to take the object’s type into account.
        if adapter.get('page_num'):
            line="当前页面是第%d页"%item['page_num']+ "\n" 
        else :
            line = json.dumps(adapter.asdict(),ensure_ascii=False) + "\n"  #非ASCII编码，便于人阅读
        self.file.write(line)
        return item
