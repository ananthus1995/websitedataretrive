import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import csv


print('Getting hcpcsdata...')
for i in range(66, 88):
        i = i - 1

        try:
            baseurls = 'https://www.hcpcsdata.com/Codes/'+chr(i)

            user_agent={'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

            reponse_page = requests.get(baseurls,headers=user_agent)

            # print(page.content)

            allcodes_data= BeautifulSoup(reponse_page.content, 'html.parser')
            # list(allcodes_data)
            # print(allcodes_data)

            for datas in allcodes_data.findAll('div', {'class': 'body-content'}):
                datas.small.decompose()
                headings= datas.find('h1').text.strip().replace("\n", "")

                catgory= datas.find('h5').text.strip().replace("\n", "").replace(",", "")

                all_table= datas.find('table', {'class':'table table-hover'})
                thead = all_table.find('thead').find_all('th')
                table_head= [th.text for th in thead]
                table_head.insert(0, 'Group')
                table_head.insert(1, 'Category')
                table_head.insert(4, 'ShortDescription')
                # print(table_head)

                all_tr_data =all_table.find('tbody').find_all('tr')
                # print(all_tr_data)

                with open('hcpcdata_file.csv','w',newline='') as myfile:
                    myfile_write =csv.writer(myfile)
                    myfile_write.writerow(table_head)

                    for tr in all_tr_data:
                        td_data = [td.text.strip().replace("\n", "") for td in tr.find_all('td')]
                        # print(td_data[0])

                        desc_url='https://www.hcpcsdata.com/Codes/'+chr(i)+'/'+td_data[0]

                        desc_reponse_page = requests.get(desc_url, headers=user_agent)

                        desc_reponse_page_data = BeautifulSoup(desc_reponse_page.content, 'html.parser')

                        for descdata in desc_reponse_page_data.findAll('div', {'class': 'body-content'}):
                            # print(descdata)
                            alldescdata_table = descdata.find('table', {'class': 'table table-hover table-condensed'})
                            # print(alldescdata_table)
                            tr_data = alldescdata_table.find('tbody').find_all('td')[1]
                            final_desctd_data=tr_data.text.strip().replace("\n", "")



                            all_hcpcdata = [headings, catgory, *td_data,final_desctd_data]
                            print(all_hcpcdata)
                            myfile_write.writerow(all_hcpcdata)


        except URLError:
            print("website  not found")