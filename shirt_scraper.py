from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time

RECIPIENT_EMAIL = 'mertzeren@gmail.com'
MAX_PRICE = 700

class ShirtScraper:
    def __init__(self):
        self.results = []
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Headless Chrome tarayıcısı kur"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(15)
            print("✓ Tarayıcı başladı")
        except Exception as e:
            print(f"✗ Tarayıcı kurma hatası: {e}")
    
    def scrape_trendyol(self):
        if not self.driver:
            return
        try:
            print("Trendyol taranıyor...")
            url = "https://www.trendyol.com/gomlek-x-c75?sort=priceasc"
            self.driver.get(url)
            time.sleep(3)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            shirts = soup.find_all('div', class_='p-card-vertical')
            
            for shirt in shirts[:20]:
                try:
                    name_elem = shirt.find('span', class_='prdct-desc-cntnr-name')
                    price_elem = shirt.find('span', class_='prc-box-discntd')
                    
                    if not price_elem:
                        price_elem = shirt.find('span', class_='prc-box')
                    
                    if name_elem and price_elem:
                        name_text = name_elem.text.strip()
                        price_text = price_elem.text.strip().replace('TL', '').replace('.', '').strip()
                        price_float = float(price_text.replace(',', '.'))
                        
                        if price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'Trendyol',
                                'name': name_text[:70],
                                'price': price_float
                            })
                except:
                    continue
            
            print(f"✓ Trendyol'dan {len([r for r in self.results if r['site'] == 'Trendyol'])} ürün eklendi")
        except Exception as e:
            print(f"✗ Trendyol hatası: {e}")
    
    def scrape_n11(self):
        if not self.driver:
            return
        try:
            print("N11 taranıyor...")
            url = "https://www.n11.com/arama?searchValue=erkek+gomlek"
            self.driver.get(url)
            time.sleep(3)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            shirts = soup.find_all('div', class_='productListContent-item')
            
            for shirt in shirts[:20]:
                try:
                    name_elem = shirt.find('h3', class_='productName')
                    price_elem = shirt.find('span', class_='productPrice')
                    
                    if name_elem and price_elem:
                        name_text = name_elem.text.strip()
                        price_text = price_elem.text.strip().replace('TL', '').replace('.', '').strip()
                        price_float = float(price_text.replace(',', '.'))
                        
                        if price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'N11',
                                'name': name_text[:70],
                                'price': price_float
                            })
                except:
                    continue
            
            print(f"✓ N11'den {len([r for r in self.results if r['site'] == 'N11'])} ürün eklendi")
        except Exception as e:
            print(f"✗ N11 hatası: {e}")
    
    def scrape_amazon(self):
        if not self.driver:
            return
        try:
            print("Amazon taranıyor...")
            url = "https://www.amazon.com.tr/s?k=erkek+gomlek&sort=price-asc-rank"
            self.driver.get(url)
            time.sleep(3)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            shirts = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for shirt in shirts[:20]:
                try:
                    name_elem = shirt.find('span', class_='a-size-base-plus')
                    if not name_elem:
                        name_elem = shirt.find('span', class_='a-size-medium')
                    
                    price_elem = shirt.find('span', class_='a-price-whole')
                    
                    if name_elem and price_elem:
                        name_text = name_elem.text.strip()
                        price_text = price_elem.text.strip().replace('₺', '').replace('.', '').strip()
                        price_float = float(price_text.replace(',', '.'))
                        
                        if 0 < price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'Amazon',
                                'name': name_text[:70],
                                'price': price_float
                            })
                except:
                    continue
            
            print(f"✓ Amazon'dan {len([r for r in self.results if r['site'] == 'Amazon'])} ürün eklendi")
        except Exception as e:
            print(f"✗ Amazon hatası: {e}")
    
    def scrape_hepsiburada(self):
        if not self.driver:
            return
        try:
            print("Hepsiburada taranıyor...")
            url = "https://www.hepsiburada.com/ara?q=erkek+gomlek"
            self.driver.get(url)
            time.sleep(3)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            shirts = soup.find_all('li', class_='productListContent-item')
            
            for shirt in shirts[:20]:
                try:
                    name_elem = shirt.find('h3', class_='productName')
                    price_elem = shirt.find('span', class_='price')
                    
                    if name_elem and price_elem:
                        name_text = name_elem.text.strip()
                        price_text = price_elem.text.strip().replace('₺', '').replace('.', '').strip()
                        price_float = float(price_text.replace(',', '.'))
                        
                        if 0 < price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'Hepsiburada',
                                'name': name_text[:70],
                                'price': price_float
                            })
                except:
                    continue
            
            print(f"✓ Hepsiburada'dan {len([r for r in self.results if r['site'] == 'Hepsiburada'])} ürün eklendi")
        except Exception as e:
            print(f"✗ Hepsiburada hatası: {e}")
    
    def scrape_akakce(self):
        if not self.driver:
            return
        try:
            print("Akakçe taranıyor...")
            url = "https://www.akakce.com/erkek-gomlek.html"
            self.driver.get(url)
            time.sleep(3)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            shirts = soup.find_all('li', class_='productListContent-item')
            
            for shirt in shirts[:20]:
                try:
                    name_elem = shirt.find('a', class_='productName')
                    price_elem = shirt.find('span', class_='productPrice')
                    
                    if name_elem and price_elem:
                        name_text = name_elem.text.strip()
                        price_text = price_elem.text.strip().replace('TL', '').replace('.', '').strip()
                        price_float = float(price_text.replace(',', '.'))
                        
                        if 0 < price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'Akakçe',
                                'name': name_text[:70],
                                'price': price_float
                            })
                except:
                    continue
            
            print(f"✓ Akakçe'den {len([r for r in self.results if r['site'] == 'Akakçe'])} ürün eklendi")
        except Exception as e:
            print(f"✗ Akakçe hatası: {e}")
    
    def scrape_cimri(self):
        if not self.driver:
            return
        try:
            print("Cimri taranıyor...")
            url = "https://www.cimri.com/erkek-gomlek"
            self.driver.get(url)
            time.sleep(3)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            shirts = soup.find_all('div', class_='productItem')
            
            for shirt in shirts[:20]:
                try:
                    name_elem = shirt.find('a', class_='productName')
                    price_elem = shirt.find('span', class_='productPrice')
                    
                    if name_elem and price_elem:
                        name_text = name_elem.text.strip()
                        price_text = price_elem.text.strip().replace('₺', '').replace('.', '').strip()
                        price_float = float(price_text.replace(',', '.'))
                        
                        if 0 < price_float < MAX_PRICE:
                            self.results.append({
                                'site': 'Cimri',
                                'name': name_text[:70],
                                'price': price_float
                            })
                except:
                    continue
            
            print(f"✓ Cimri'den {len([r for r in self.results if r['site'] == 'Cimri'])} ürün eklendi")
        except Exception as e:
            print(f"✗ Cimri hatası: {e}")
    
    def close(self):
        if self.driver:
            self.driver.quit()
    
    def run(self):
        try:
            self.scrape_trendyol()
            self.scrape_n11()
            self.scrape_amazon()
            self.scrape_hepsiburada()
            self.scrape_akakce()
            self.scrape_cimri()
        finally:
            self.close()
        return self.results

def send_email(results):
    if not results:
        print("Ürün bulunamadı, mail gönderilmiyor")
        return
    
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if not sender_email or not sender_password:
        print("Email credentials bulunamadı")
        return
    
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
                <th>Fiyat (TL)</th>
            </tr>
    """
    
    for item in sorted(results, key=lambda x: x['price']):
        html_content += f"<tr><td><strong>{item['site']}</strong></td><td>{item['name']}</td><td>{item['price']:.0f}</td></tr>"
    
    html_content += """
        </table>
        <p style="margin-top: 30px; color: #666; font-size: 12px;">
            Otomatik olarak gönderilen rapor.
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
    print("Script başladı...")
    scraper = ShirtScraper()
    results = scraper.run()
    print(f"Toplam {len(results)} ürün bulundu")
    send_email(results)

# Test modu - hata ayıklama için
if __name__ == "__main__":
    print("Script başladı...")
    scraper = ShirtScraper()
    
    # Trendyol test
    print("\n=== TRENDYOL TEST ===")
    try:
        scraper.driver.get("https://www.trendyol.com/gomlek-x-c75?sort=priceasc")
        time.sleep(3)
        soup = BeautifulSoup(scraper.driver.page_source, 'html.parser')
        print(f"HTML uzunluğu: {len(scraper.driver.page_source)} karakter")
        
        # Farklı class'ları ara
        test_classes = ['p-card-vertical', 'p-card', 'productCard', 'productItem']
        for cls in test_classes:
            found = soup.find_all('div', class_=cls)
            print(f"  {cls}: {len(found)} bulundu")
    except Exception as e:
        print(f"Hata: {e}")
    
    scraper.close()
