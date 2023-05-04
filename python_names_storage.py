from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "hazel-lyceum-343617",
  "private_key_id": "72cd7589c5dd60526194a289c729006aa0d8fef2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCh6tX1K2uKxab2\nGkKWgfRAgbludd9ovsFx5ET/aKeha/otwrXGE7mdQait/Ppk9TTBiKgXhY/AXAik\nEggYqQCotKGjxX9ieNTa1RYMS4VvAt5wJoaUDwh848loB+fXVSYKMV8U0KPWmcg1\nD5kGtuOJXyT2lcJaHWMFwzP2ejaO4d8DAfQebSksusaT98D22qWgEC2sS0NAmlmM\n1FmpICUbomZDALB3C8E/7jUo/QK9cH4Wf+8dOnrXN8NqICmpTJIXWMzChLS03Blj\nK6l5npjEiuklxj0d4lp4OHzccXY1IPjjl1thePjfmqphliSGPU17t6Navr2TUdd3\nSab13li1AgMBAAECggEABtpXVWHR0qUEaMCaRl/4LD3BUSNEghymt9ELOYseoyac\nh1DJHDnL/pOflcOR/nFhWvqTcLFqsN/ETttjg9WtTTad675JYqvOCHgBz6Hnoxfq\nPbFnuz76ozyJ0vEYtySnsEFALrOY55WJI3PGTIIzlaYU/KnAeMtrHDyTh7BK/FeS\nOmEpXlHrvI7Vqgo9SEhZw+nymPWQ0bOZOh1m3Yuc7tOmS7DuWax18eqjnOyrPBkC\nEXBbFS64ErLMtsHuK2LZ4kphY3uyeqUOPuPLkzyIT3HR7IjtLVKrqoTlCVUW8VtC\nFaqFwt69P8FD1kpWxSxc0Qg+6xckdn4/o6CS4cr6aQKBgQDNuoS3j+SbsqR+OBsX\nkBFhNgPQoS5jWjxc00f68Kxb+EZReDTRQHDib3M1NDOX3DJwiclX5pO9MvUDj8uK\niedlKVB8dvrUtZBr1SpAurf//9879+gXgxguQL9vOc8CDmKFpM/V8lYz59CMzlE4\nQqHLXnmr1boZ7qNMTphA4GCMDQKBgQDJe60jIatRsg6CbFhl4vSMcsAayPgdsGIC\nMlNzGWiwemiBqt1nZ//l6MTg2Ok+ghCm8metbf/xN+tmws4t5SIBvw24KUomSyhu\ni89L/kYMHVRyp7uEY/VMS1tIiz/hr57Gl/LKaR0VFFpojxOh5a+s5vHIazF9NqXm\n4y0SVvDNSQKBgFlW4kOErVYf4eceHkXBPorklguHs0lZ6lS1O9DxqyfVTVQby3QD\ndAIhO/qizLTp3s2YSGNvskC7XENLsqxa7q2zn0wtrweoQStSyqKJc1Ysm5jDM3ri\nZyHO5FM823SdIpO+2rKiJmUsChjbj9HKvdA/Gr9QdRzF0QxWJTAnQEYRAoGAJOkZ\nUMRMRE0gR1hd4VxwfIJRGxcSDS5Q5iIeE4nmGd5y4r5QjS8KPC4mUyKpqB/fuRXT\nVHxAVQpvf4XUi6fcUQGVG9XElbtTDt1h/oP4hSOiYtbDjX9aYr2zXVjVPR0VM0CG\n4/nZsBDodxsu94vCYSR1yseIa23leqTHjwKKXrECgYB6NfjapGs/k3ydzJLiQ/lF\nxW7YG7G4zNK/5gpucVf6M/BWbzwo0dcvzKlb+cbOoEVtziZIH0CNEmpdE4yQyCGe\n/DoXx3ajigfNf59/GYVqQbSUPZawObZNFYjwfYYH+uH53ktLv61oITby0tYGJk45\nqAUaup7M6LYBu7KWmPQDnA==\n-----END PRIVATE KEY-----\n",
  "client_email": "908573186440-compute@developer.gserviceaccount.com",
  "client_id": "110252518196254568444",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/908573186440-compute%40developer.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('atividade_iv') ### Nome do seu bucket
  blob = bucket.blob('atividade_iv.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
