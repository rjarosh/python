import requests, bs4, os

url = "https://xkcd.com"
os.makedirs('xkcd', exist_ok=True) #if the folder exists, keep moving

while not url.endswith("#"):
    #main loop. Keep going until the url ends with # which signifies no more comics
    print('Downloading page %s...' % url)
    res=requests.get(url)
    res.raise_for_status

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image')
    else:
        comicUrl = 'https:' + comicElem[0].get('src')
        print('Downloading image %s...' % (comicUrl))
        res=requests.get(comicUrl)
        res.raise_for_status
        #create the file now. .basename gets the filename from the url (e.x. google.com/photo.png)
        imageFile = open(os.path.join('xkcd',os.path.basename(comicUrl)), 'wb')
        #write to the file
        for chunk in res.iter_content(100_000):
            imageFile.write(chunk)
        imageFile.close()

    #get previous photo
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'https://xkcd.com' + prevLink.get('href')

print('Done.')
