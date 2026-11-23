"""Exercise actual bundled Mermaid at the published subpath; no upstream APIs."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re, shutil, tempfile, threading
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args): pass

def main():
 screenshots=ROOT/'browser-checks';screenshots.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as temporary:
  shutil.copytree(ROOT/'dist',Path(temporary)/'example-tool')
  server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=temporary));threading.Thread(target=server.serve_forever,daemon=True).start()
  try:
   with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':1000});errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(f'http://127.0.0.1:{server.server_port}/example-tool/')
    expect(page.locator('#status')).to_contain_text('Diagram ready',timeout=30000)
    expect(page.locator('#diagram')).to_be_visible()
    assert page.locator('#diagram').evaluate('(e)=>e.naturalWidth')>100
    page.locator('#code').fill('flowchart LR\n Test[Independent custom source] --> Result[Rendered locally]')
    page.locator('#render').click();expect(page.locator('#status')).to_contain_text('Diagram ready',timeout=30000)
    with page.expect_download() as download:page.locator('#svg').click()
    svg=Path(download.value.path()).read_text()
    # Mermaid wraps visible labels across SVG tspans; assert their rendered text,
    # rather than requiring the sentence to be contiguous in serialized markup.
    document=ET.fromstring(svg)
    text=' '.join(' '.join(document.itertext()).split())
    assert 'Independent custom source' in text, text[-2000:]
    assert 'Rendered locally' in text, text[-2000:]
    for element in document.iter():
     assert element.tag.rsplit('}',1)[-1].lower() not in {'script','foreignobject','iframe'}, element.tag
     for key,value in element.attrib.items():
      name=key.rsplit('}',1)[-1].lower()
      assert not name.startswith('on'), key
      if name=='href': assert not value or re.fullmatch(r'#[\w:.-]+',value), value
    previous=page.locator('#diagram').get_attribute('src')
    page.locator('#code').fill('flowchart LR\n A[unterminated')
    page.locator('#render').click();expect(page.locator('#status')).to_contain_text('previous diagram is unchanged',timeout=30000)
    assert page.locator('#diagram').get_attribute('src')==previous
    with page.expect_download() as download:page.locator('#project').click()
    project=Path(download.value.path()).read_bytes()
    page.locator('#file').set_input_files({'name':'reopen.json','mimeType':'application/json','buffer':project})
    expect(page.locator('#status')).to_contain_text('Source opened locally')
    assert 'Independent custom source' in page.locator('#code').input_value()
    page.locator('#render').click();expect(page.locator('#status')).to_contain_text('Diagram ready',timeout=30000)
    with page.expect_download() as download:page.locator('#png').click()
    assert Path(download.value.path()).read_bytes().startswith(b'\x89PNG')
    page.screenshot(path=str(screenshots/'desktop.png'),full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(screenshots/'mobile.png'),full_page=True)
    assert not errors,errors
    browser.close()
  finally:server.shutdown()
 print('Browser checks passed: actual local Mermaid, exports, error preservation, project import and mobile width')
if __name__=='__main__':main()
