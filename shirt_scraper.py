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
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36'
        }
    
    def scrape_trendyol(self):
        """Trendyol API'sini kullan"""
        try:
            print("Trendyol API'si sorgulanıyor...")
            url = "https://api.trendyol.com/v2/productSearch"
            params = {
                'q': 'erkek gomlek',
                'pi': 1,
                'ps': 24,
                'sortBy': 'price-asc'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'products' in data:
                for product in data['products'][:20]:
                    try:
                        name = product.get('name', '')
                        price = product.get('discountedPrice', product.get('originalPrice', 0))
                        
                        if price and price < MAX_PRICE and 'gömlek' in name.lower():
                            self.results.append({
                                'site': 'Trendyol',
                                'name': name[:70],
                                'price': float(price)
                            })
                    except:
                        continue
            
            print(f"✓ Trendyol'dan {len([r for r in self.results if r['site'] == 'Trendyol'])} ürün eklendi")
        except Exception as e:
            print(f"✗ Trendyol hatası: {e}")
    
    def scrape_n11(self):
        """N11 API'sini kullan"""
        try:
            print("N11 API'si sorgulanıyor...")
            url = "https://api.n11.com/v1/products/search"
            params = {
                'keyword': 'erkek gomlek',
                'page': 0,
                'pageSize': 24,
                'sortBy': 'price'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'result' in data and 'products' in data['result']:
                for product in data['result']['products'][:20]:
                    try:
                        name = product.get('title', '')
                        price = product.get('prices', {}).get('salePrice', product.get('prices', {}).get('listPrice', 0))
                        
                        if price and price < MAX_PRICE and 'gömlek' in name.lower():
                            self.results.append({
                                'site': 'N11',
                                'name': name[:70],
                                'price': float(price)
                            })
                    except:
                        continue
            
            print(f"✓ N11'den {len([r for r in self.results if r['site'] == 'N11'])} ürün eklendi")
        except Exception as e:
            print(f"✗ N11 hatası: {e}")
    
    def scrape_akakce(self):
        """Akakçe'den basit HTML scraping"""
        try:
            print("Akakçe taranıyor...")
            url = "https://www.akakce.com/erkek-gomlek.html"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = soup.find_all('li', class_='productListContent-item')
            
            for product in products[:30]:
                try:
                    name_elem = product.find('a', class_='productName')
                    price_elem = product.find('span', class_='productPrice')
                    
                    if name_elem and price_elem:
                        name_text = name_elem.text.strip()
                        price_text = price_elem.text.strip()
                        price_text = price_text.replace('TL', '').replace('.', '').replace(',', '.').strip()
                        
                        try:
                            price_float = float(price_text)
                            
                            if 0 < price_float < MAX_PRICE:
                                self.results.append({
                                    'site': 'Akakçe',
                                    'name': name_text[:70],
                                    'price': price_float
                                })
                        except ValueError:
                            continue
                except:
                    continue
            
            print(f"✓ Akakçe'den {len([r for r in self.results if r['site'] == 'Akakçe'])} ürün eklendi")
        except Exception as e:
            print(f"✗ Akakçe hatası: {e}")
    
    def run(self):
        try:
            self.scrape_trendyol()
            self.scrape_n11()
            self.scrape_akakce()
        except Exception as e:
            print(f"Scraping hatası: {e}")
        
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
    
    unique_results = []
    seen = set()
    
    for item in sorted(results, key=lambda x: x['price']):
        key = (item['name'].lower(), round(item['price'], -1))
        if key not in seen:
            seen.add(key)
            unique_results.append(item)
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h2 {{ color: #333; border-bottom: 3px solid #2196F3; padding-bottom: 10px; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #2196F3; color: white; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #f0f0f0; }}
            .price {{ font-weight: bold; color: #d32f2f; }}
            .site {{ font-weight: bold; color: #1976d2; }}
            .footer {{ margin-top: 30px; color: #666; font-size: 12px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>📊 Günlük Gömlek İndirim Raporu</h2>
            <p><strong>Tarih:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
            <p><strong>Bulunan Ürün:</strong> {len(unique_results)} adet</p>
            <table>
                <tr>
                    <th>Site</th>
                    <th>Ürün Adı</th>
                    <th>Fiyat</th>
                </tr>
    """
    
    for item in unique_results[:50]:
        html_content += f"<tr><td><span class='site'>{item['site']}</span></td><td>{item['name']}</td><td><span class='price'>{item['price']:.0f} TL</span></td></tr>"
    
    html_content += """
            </table>
            <div class="footer">
                <p>Otomatik olarak gönderilen rapor. Her gün saat 14:00'de çalışır.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"Gömlek İndirim Raporu - {datetime.now().strftime('%d.%m.%Y')} ({len(unique_results)} ürün)"
        msg.attach(MIMEText(html_content, 'html'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"✓ Email gönderildi: {RECIPIENT_EMAIL} ({len(unique_results)} ürün)")
    except Exception as e:
        print(f"✗ Email hatası: {e}")

if __name__ == "__main__":
    print("Script başladı...")
    print(f"Max fiyat: {MAX_PRICE} TL")
    print("-" * 50)
    
    scraper = ShirtScraper()
    results = scraper.run()
    
    print("-" * 50)
    print(f"Toplam {len(results)} ürün bulundu")
    
    send_email(results)
    
    print("Script bitti.")
