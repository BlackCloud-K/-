from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
import datetime

# 货币代码转换表
currency_dict = {
    'GBP': '英镑',
    'HKD': '港币',
    'USD': '美元',
    'CHF': '瑞士法郎',
    'DEM': '德国马克',
    'FRF': '法国法郎',
    'SGD': '新加坡元',
    'SEK': '瑞典克朗',
    'DKK': '丹麦克朗',
    'NOK': '挪威克朗',
    'JPY': '日元',
    'CAD': '加拿大元',
    'AUD': '澳大利亚元',
    'EUR': '欧元',
    'MOP': '澳门元',
    'PHP': '菲律宾比索',
    'THB': '泰国铢',
    'NZD': '新西兰元',
    'KRW': '韩元',
    'RUB': '卢布',
    'MYR': '林吉特',
    'TWD': '新台币',
    'ESP': '西班牙比塞塔',
    'ITL': '意大利里拉',
    'NLG': '荷兰盾',
    'BEF': '比利时法郎',
    'FIM': '芬兰马克',
    'INR': '印度卢比',
    'IDR': '印尼卢比',
    'BRL': '巴西里亚尔',
    'AED': '阿联酋迪拉姆',
    'ZAR': '南非兰特',
    'SAR': '沙特里亚尔',
    'TRY': '土耳其里拉'
}

# 设置
edge_options = Options()
edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
edge_options.add_argument('--disable-blink-features=AutomationControlled')
edge_options.add_argument('headless')
br = webdriver.Edge(options=edge_options)

# 获取输入
date, cur_code = input("请输入待查询日期与货币代码: ").split()
formatted_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
try:
    datetime.datetime.strptime(formatted_date, '%Y-%m-%d')
except ValueError:
    raise ValueError("日期格式错误")
try:
    cur = currency_dict[cur_code]
except KeyError:
    raise NameError('找不到对应的货币')

# 搜索目标
url = "https://www.boc.cn/sourcedb/whpj/"
try:
    br.get(url)
except TimeoutException:
    raise NameError('页面加载超时')
input_date_start = br.find_elements('xpath', '//*[@id="historysearchform"]/div/table/tbody/tr/td[2]/div/input')
input_date_end = br.find_elements('xpath', '//*[@id="historysearchform"]/div/table/tbody/tr/td[4]/div/input')
input_date_start[0].send_keys(formatted_date)
input_date_end[0].send_keys(formatted_date)
select = Select(br.find_elements('xpath', '//*[@id="pjname"]')[0])
select.select_by_value(cur)
button = br.find_elements('xpath', '//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input')
button[0].click()

# 获取结果
try:
    result = br.find_elements('xpath', '/html/body/div/div[4]/table/tbody/tr[2]/td[4]')[0].text
    result = formatted_date + cur + "现汇卖出价：" + result
except IndexError:
    raise NameError('该日期找不到数据')

# 写入文件
with open('result.txt', 'a', encoding='utf-8') as f:
    f.write(result + '\n')

