import APE

pages = ['https://google.com',
         'https://yandex.ru',
         'https://example.com',
         'haweg weas f',
         'http://wetewt.de',  # throw a couple of non-existing pages
         'https://pymotw.com/',
         'https://xkcd.com/',
         'https://vk.com/',
         'https://students.superjob.ru',
         'https://www.reddit.com',
         'https://git-scm.com',
         'https://habrahabr.ru/',
         'https://appvelox.ru/',
         ]
ape = APE.APE(10)
results = ape.get_pages(pages)
for r in results:
    if r['status_code'] != -1:
        print('url: {}, code: {}, content: {}'.format(r['url'], r['status_code'], r['content'][:100]))
    else:
        print('ERROR: url: {}, {}'.format(r['url'], r['err']))
