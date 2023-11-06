from bs4 import BeautifulSoup
import glob
import jsonlines

documents = []

for file_path in glob.glob("data/*.html"):
    with open(file_path, "r") as html_file:
        contents = html_file.read()
    soup = BeautifulSoup(contents)         
    title = soup.select_one("title").text
    url = soup.select_one("meta[property='og:url']")["content"]
    body = [element.text for element in soup.select("div[data-component='text-block']")]
    print(title, url, body)

    documents.append({
        "url": url,
        "title": title,
        "body": body
    })

with jsonlines.open('data/documents.json', mode='w') as writer:
    for document in documents:
        writer.write(document)


