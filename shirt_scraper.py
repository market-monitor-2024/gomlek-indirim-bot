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
        """Chrome tarayıcısını kur"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(20)
            print("✓ Tarayıcı başladı")
        except Exception as e:
            print(f"✗ Tarayıcı kurma hatası: {e}")
    
    def scrape_akakce(self):
        """Akakçe'den erkek gömlekleri çek"""
        if not self.driver:
            return
        
        try:
            print("\nAkakçe'den gömlekler taranıyor...")
            url = "https://www.akakce.com/erkek-gomlek.html"
            
            self.driver.get(url)
            time.sleep(4)
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            products = soup.find_all('li', class_='productListContent-item')
            print(f"  {len(products)} ürün bulundu")
            
            for idx, product in enumerate(products):
                try:
                    name_elem = product.find('a', class_='productName')
                    if not name_elem:
                        continue
                    
                    name_text = name_elem.text.strip()
                    
                    price_elem = product.find('span', class_='productPrice')
                    if not price_elem:
                        continue
                    
                    price_text = price_elem.text.strip()
                    price_clean = price_text.replace('TL', '').replace('.', '').replace(',', '.').strip()
                    
                    try:
                        price_float = float(price_clean)
                    except ValueError:
                        continue
                    
                    if 0 < price_float < MAX_PRICE:
                        self.results.append({
                            'site': 'Akakçe',
                            'name': name_text[:75],
                            'price': price_float,
                            'url': name_elem.get('href', '')
                        })
                        print(f"  [{idx+1}] {name_text[:60]}... - {price_float:.0f} TL")
                
                except Exception as e:
                    continue
            
            akakce_count = len([r for r in self.results if r['site'] == 'Akakçe'])
            print(f"\n✓ Akakçe'den {akakce_count} ürün eklendi")
            
        except Exception as e:
            print(f"✗ Akakçe hatası: {e}")
    
    def close(self):
        """Tarayıcıyı kapat"""
        if self.driver:
            self.driver.quit()
            print("✓ Tarayıcı kapatıldı")
    
    def run(self):
        """Scraping işlemini çalıştır"""
        try:
            self.scrape_akakce()
        finally:
            self.close()
        
        return self.results

def send_email(results):
    """E-mail gönder"""
    if not results:
        print("\n⚠ Ürün bulunamadı, mail gönderilmiyor")
        return
    
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if not sender_email or not sender_password:
        print("✗ Email credentials bulunamadı")
        return
    
    sorted_results = sorted(results, key=lambda x: x['price'])[:50]
    
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 900px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a73e8; border-bottom: 4px solid #1a73e8; padding-bottom: 15px; margin-bottom: 20px; }}
            .info {{ background-color: #f0f8ff; padding: 15px; border-left: 4px solid #1a73e8; margin-bottom: 20px; border-radius: 4px; }}
            .info p {{ margin: 8px 0; color: #333; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th {{ background-color: #1a73e8; color: white; padding: 14px; text-align: left; font-weight: 600; }}
            td {{ border-bottom: 1px solid #ddd; padding: 12px 14px; }}
            tr:hover {{ background-color: #f9f9f9; }}
            .price {{ font-weight: bold; color: #d32f2f; font-size: 16px; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Günlük Gömlek İndirim Raporu</h1>
            <div class="info">
                <p><strong>📅 Tarih:</strong> {datetime.now().strftime('%d.%m.%Y saat %H:%M')}</p>
                <p><strong>🔍 İncelenen Site:</strong> Akakçe (Tüm Siteler)</p>
                <p><strong>💰 Fiyat Aralığı:</strong> 0 - {MAX_PRICE} TL</p>
                <p><strong>📦 Bulunan Ürün:</strong> <strong>{len(sorted_results)}</strong> adet</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th style="width: 15%;">Sıra</th>
                        <th style="width: 60%;">Ürün Adı</th>
                        <th style="width: 25%;">Fiyat</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for idx, item in enumerate(sorted_results, 1):
        html_content += f"<tr><td>{idx}</td><td>{item['name']}</td><td><span class='price'>{item['price']:.0f} TL</span></td></tr>"
    
    html_content += """
                </tbody>
            </table>
            <div class="footer">
                <p>✅ Bu email otomatik olarak gönderilmiştir.</p>
                <p>🔄 Her gün saat 14:00'de yeni tarama yapılır.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"Gömlek İndirim Raporu - {datetime.now().strftime('%d.%m.%Y')} ({len(sorted_results)} ürün)"
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        print(f"\n📧 Email gönderiliyor ({len(sorted_results)} ürün)...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"✓ Email başarıyla gönderildi: {RECIPIENT_EMAIL}")
        
    except Exception as e:
        print(f"✗ Email gönderme hatası: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Gömlek İndirim Bot")
    print("=" * 60)
    print(f"⏰ Başlangıç: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"💰 Max Fiyat: {MAX_PRICE} TL")
    print("=" * 60)
    
    scraper = ShirtScraper()
    results = scraper.run()
    
    print("=" * 60)
    print(f"📊 Toplam {len(results)} ürün bulundu")
    print("=" * 60)
    
    send_email(results)
    
    print(f"⏱ Bitiş: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print("=" * 60)
