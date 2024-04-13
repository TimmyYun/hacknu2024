import requests as r
import json
from bs4 import BeautifulSoup

def parsePartners():
    response = r.get('https://club.forte.kz/partneroffers')
    
    if response.status_code == 200:
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

        if script_tag:
            json_string = script_tag.string
            parsed_json = json.loads(json_string)
            partners = parsed_json['props']['pageProps']['dynamicComponents'][2]['partners']
            
            partners = [partner for partner in partners if partner.get("cashbak", 0) != 0]
            
            for i in range(len(partners)):
                new_token = {}
                new_token["title"] = partners[i]["title"]
                new_token["cashback"] = partners[i].get("cashbak", 0)
                new_token["address"] = partners[i].get("addresses", "")

                sub_category = partners[i].get("subCategory", {})
                parent_category = sub_category.get("parentCategory")

                if parent_category is None:
                    new_token["category"] = sub_category.get("title", "")
                else:
                    new_token["category"] = parent_category.get("title", "")

                partners[i] = new_token
            
            return partners
        else:
            print("No script tag found with id '__NEXT_DATA__'")
    else:
        print("Failed to fetch data from 'https://club.forte.kz/partneroffers'")
