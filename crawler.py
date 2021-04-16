from requests_html import HTMLSession

url = 'http://konect.cc/networks/'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76'}

session = HTMLSession()
r = session.get(url=url, headers=headers) 
r.html.render() 
data_name = r.html.xpath("//div[@id='page']/table[1]/tbody[1]/tr/td[2]")[1:]
node_num = r.html.xpath("//div[@id='page']//table/tbody[1]/tr/td[4]")[1:]
edge_num = r.html.xpath("//div[@id='page']//table/tbody[1]/tr/td[5]")[1:]
avaliable_img = r.html.xpath("//div[@id='page']//table/tbody[1]/tr/td[3]/img[1]")
test_img = r.html.xpath("//div[@id='page']//table/tbody[1]/tr/td[3]/img[2]")
first_data_types_img = r.html.xpath("//div[@id='page']//table/tbody[1]/tr/td[3]/img[3]")
second_data_types_img = r.html.xpath("//div[@id='page']//table/tbody[1]/tr/td[3]/img[4]")


data_len = len(avaliable_img)

avaliable = []
pass_test = []
first_data_types = []
second_data_types = []
for i in range(data_len):
    if(avaliable_img[i].attrs['title'] == 'Dataset is available for download'):
        avaliable.append(1)
    else:
        avaliable.append(0)
    if(first_data_types_img[i].attrs['title'] == 'Bipartite, undirected'):
        first_data_types.append(1)
    else:
        first_data_types.append(0)
    if(second_data_types_img[i].attrs['title'] == 'Unweighted, multiple edges'):
        second_data_types.append(1)
    else:
        second_data_types.append(0)
    if(test_img[i].attrs['title'] == 'Dataset passed all tests'):
        pass_test.append(1)
    else:
        pass_test.append(0)
    
atb_idx = [] #avaliable_temporal_bipartite_graph
for i in range(data_len):
    flag = avaliable[i] * pass_test[i] * first_data_types[i] * second_data_types[i]
    if(flag):
        try:
            timestamp = r.html.xpath("//div[@id='page']//table/tbody[1]/tr[{}]/td[3]/img[5]".format(i+2))[0].attrs['title']
            if(timestamp == 'Edges are annotated with timestamps'):
                atb_idx.append(1)
                continue
        except:
            pass
    atb_idx.append(0)

# print(atb_idx[10:20])
# print(data_name[12].text)
# print(node_num[12].text)
# print(edge_num[12].text)