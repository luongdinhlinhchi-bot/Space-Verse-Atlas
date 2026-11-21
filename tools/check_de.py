import sys
from playwright.sync_api import sync_playwright
cities=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':900,'height':1000}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///home/claude/wm/dist/index.html')
    pick=lambda c: pg.evaluate("c=>document.querySelector('[data-code='+c+']').dispatchEvent(new MouseEvent('click',{bubbles:true}))",c)
    pick('DEU'); print({k:pg.locator('.city-marker.'+k).count() for k in('done','partial','todo')})
    for c in cities:
        pg.locator(f'[data-city={c}]').dispatch_event('click'); print(c, pg.locator('#city-panel .unit-count').all_inner_texts(), pg.locator('.researcher-list li').count())
    pick('FIN'); pg.locator('[data-city=helsinki]').dispatch_event('click'); print('FIN helsinki', pg.locator('.researcher-list li').count(), errs)
    b.close()
