import scrapy
from tieba.items import TiebaItem
from lxml import etree
class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    allowed_domains = ['baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw=%E7%AC%91%E8%AF%9D%E5%A4%A7%E5%85%A8&fr=index']
    count = 0
    maxpage =input("请输入最大页数:")
    def parse(self, response):
        XiaohuaSpider.count+=1
        pagenum= XiaohuaSpider.count
        #有输入并且当前页数超过页数就停止
        if XiaohuaSpider.maxpage and pagenum>int(XiaohuaSpider.maxpage): 
            print('超过页数，停止')
            return 
        print('performing page %d'%pagenum)
        item = TiebaItem()  #实例化item
        page_item=dict() #记录页数
        page_item['page_num']=pagenum
        yield page_item   #返回到pipline写出当前页码
        #将注释符号去掉，并替换response中的body， byte类型
        newbody  =bytes( response.text.replace("<!--","").replace("-->",""),encoding='utf-8')
        # 提取数据
        newresponse=response.replace(body=newbody)
        li_list = newresponse.xpath('//li[@class=" j_thread_list clearfix"]')
        #print(len(li_list))

        for el in li_list:
            item['title'] = el.xpath(".//a/text()").get() #每个结果都是列表
            item['link'] = newresponse.urljoin(el.xpath(".//a/@href").get())
            yield item
        #下一页
        next_part_url= newresponse.xpath('//*[@id="frs_list_pager"]/a[contains(text(),"下一页>")]/@href').get()
        # 只要还有下一页就进行请求
        if next_part_url!=None:
            next_url='https:'+next_part_url
            yield scrapy.Request(url=next_url,callback=self.parse)
        
   
        

