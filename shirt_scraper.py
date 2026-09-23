import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

RECIPIENT_EMAIL = 'mertzeren@gmail.com'
MAX_PRICE = 700

class ShirtScraper:
    def __init__(self):
        self.results = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_trendyol(self):
        try:
            url = "https://www.trendyol.com/gomlek-x-c75?sort=priceasc"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            shirts = soup.find_all('div', class_='p-card')
            
            for shirt in shirts[:15]:
                try:
                    name = shirt.find('span', class_='prdct-desc-cntnr-name')
                    price = shirt.find('span', class_='prc-box-discntd')
                    
                    if name and price:
                        name_text = name.text.strip()
                        price_text = price.text.strip().replace('TL', '').strip()
                        price_float = float(price_text.replace('.', '').replace(',', '.'))
                        
                        if price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'Trendyol',
                                'name': name_text[:60],
                                'price': price_float
                            })
                except:
                    continue
        except Exception as e:
            print(f"Trendyol hatası: {e}")
    
    def scrape_n11(self):
        try:
            url = "https://www.n11.com/arama?searchValue=erkek+gomlek"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            shirts = soup.find_all('div', class_='productListItem')
            
            for shirt in shirts[:15]:
                try:
                    name = shirt.find('h3', class_='prdName')
                    price = shirt.find('span', class_='prc')
                    
                    if name and price:
                        name_text = name.text.strip()
                        price_text = price.text.strip().replace('TL', '').strip()
                        price_float = float(price_text.replace('.', '').replace(',', '.'))
                        
                        if price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'N11',
                                'name': name_text[:60],
                                'price': price_float
                            })
                except:
                    continue
        except Exception as e:
            print(f"N11 hatası: {e}")
    
    def scrape_amazon(self):
        try:
            url = "https://www.amazon.com.tr/s?k=erkek+gomlek&sort=price-asc-rank"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            shirts = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for shirt in shirts[:15]:
                try:
                    name = shirt.find('span', class_='a-size-medium')
                    price = shirt.find('span', class_='a-price-whole')
                    
                    if name and price:
                        name_text = name.text.strip()
                        price_text = price.text.strip().replace('₺', '').replace('.', '').strip()
                        price_float = float(price_text.replace(',', '.')) if price_text else 0
                        
                        if 0 < price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'Amazon',
                                'name': name_text[:60],
                                'price': price_float
                            })
                except:
                    continue
        except Exception as e:
            print(f"Amazon hatası: {e}")
    
    def scrape_hepsiburada(self):
        try:
            url = "https://www.hepsiburada.com/ara?q=erkek+gomlek"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            shirts = soup.find_all('li', class_='productListContent-item')
            
            for shirt in shirts[:15]:
                try:
                    name = shirt.find('h3', class_='productName')
                    price = shirt.find('div', class_='productPrice')
                    
                    if name and price:
                        name_text = name.text.strip()
                        price_text = price.text.strip().replace('₺', '').replace('.', '').strip()
                        price_float = float(price_text.replace(',', '.')) if price_text else 0
                        
                        if 0 < price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'Hepsiburada',
                                'name': name_text[:60],
                                'price': price_float
                            })
                except:
                    continue
        except Exception as e:
            print(f"Hepsiburada hatası: {e}")
    
    def scrape_akakce(self):
        try:
            url = "https://www.akakce.com/erkek-gomlek.html"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            shirts = soup.find_all('div', class_='productListItem')
            
            for shirt in shirts[:15]:
                try:
                    name = shirt.find('a', class_='productName')
                    price = shirt.find('span', class_='productPrice')
                    
                    if name and price:
                        name_text = name.text.strip()
                        price_text = price.text.strip().replace('TL', '').replace('.', '').strip()
                        price_float = float(price_text.replace(',', '.')) if price_text else 0
                        
                        if 0 < price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'Akakçe',
                                'name': name_text[:60],
                                'price': price_float
                            })
                except:
                    continue
        except Exception as e:
            print(f"Akakçe hatası: {e}")
    
    def scrape_cimri(self):
        try:
            url = "https://www.cimri.com/erkek-gomlek"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            shirts = soup.find_all('div', class_='productItem')
            
            for shirt in shirts[:15]:
                try:
                    name = shirt.find('a', class_='productName')
                    price = shirt.find('span', class_='productPrice')
                    
                    if name and price:
                        name_text = name.text.strip()
                        price_text = price.text.strip().replace('₺', '').replace('.', '').strip()
                        price_float = float(price_text.replace(',', '.')) if price_text else 0
                        
                        if 0 < price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'Cimri',
                                'name': name_text[:60],
                                'price': price_float
                            })
                except:
                    continue
        except Exception as e:
            print(f"Cimri hatası: {e}")
    
    def run(self):
        self.scrape_trendyol()
        self.scrape_n11()
        self.scrape_amazon()
        self.scrape_hepsiburada()
        self.scrape_akakce()
        self.scrape_cimri()
        return self.results

def send_email(results):
    if not results:
        print("Ürün bulunamadı")
        return
    
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #2196F3; color: white; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h2>📊 Günlük Gömlek İndirim Raporu</h2>
        <p><strong>Tarih:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <p><strong>Bulunan Ürün:</strong> {len(results)} adet</p>
        <table>
            <tr>
                <th>Site</th>
                <th>Ürün Adı</th>
                <th>Fiyat</th>
            </tr>
    """
    
    for item in sorted(results, key=lambda x: x['price']):
        html_content += f"<tr><td><strong>{item['site']}</strong></td><td>{item['name']}</td><td>{item['price']:.0f} TL</td></tr>"
    
    html_content += """
        </table>
        <p style="margin-top: 30px; color: #666; font-size: 12px;">
            Bu email otomatik olarak gönderilmiştir.
        </p>
    </body>
    </html>
    """
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"Gömlek İndirim Raporu - {datetime.now().strftime('%d.%m.%Y')}"
        
        msg.attach(MIMEText(html_content, 'html'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"✓ Email gönderildi: {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"✗ Email hatası: {e}")

if __name__ == "__main__":
    scraper = ShirtScraper()
    results = scraper.run()
    print(f"Toplam {len(results)} ürün bulundu")
    send_email(results)
