from playwright.sync_api import sync_playwright, expect
from pathlib import Path
import json
out=Path('/workspace/wk5-photoshare/drafts/phou-period-example/verification')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);q=b.new_page(viewport={'width':390,'height':844});errors=[];q.on('pageerror',lambda e:errors.append(str(e)))
 q.goto('http://127.0.0.1:8123/drafts/phou-period-example/');q.locator('.make-album').click();expect(q.locator('#s-create')).to_contain_text('모임 기간')
 q.locator('#fname').fill('가을 모임');q.locator('#eventStart').fill('2026-10-25T09:00');q.locator('#eventEndMode').select_option('date');q.locator('#eventEnd').fill('2026-10-29T23:59');q.locator('#next1').click();q.locator('#mode-later').click();q.locator('#optionsNext').click();q.locator('#s-share .bottom .main').click()
 q.get_by_role('button',name='앨범 메뉴',exact=True).click();q.get_by_role('button',name='앨범 정보·비밀번호 수정',exact=False).click();expect(q.locator('#dialogContent .collection-period-form>b')).to_have_text('모임 기간');q.screenshot(path=str(out/'01-meeting-info.png'));q.locator('#dialogContent').get_by_role('button',name='닫기',exact=True).click()
 q.locator('#albumAddFab').click();expect(q.locator('#s-options .photo-period-value')).to_contain_text('2026.10.29');q.locator('#s-options').get_by_role('button',name='기간 변경',exact=True).click();q.locator('#batchEnd').fill('2026-10-26T23:59');q.get_by_role('button',name='기간 적용',exact=True).click()
 expect(q.locator('#s-options .photo-period-value')).to_contain_text('2026.10.26');assert q.evaluate("cur.eventEnd==='2026-10-29T23:59'");q.screenshot(path=str(out/'02-upload-range.png'))
 q.locator('#optionsNext').click();expect(q.locator('#foundTitle')).to_be_visible(timeout=9000);expect(q.locator('#s-import .photo-period-value')).to_contain_text('2026.10.26');q.locator('#sharebtn').click();expect(q.locator('#s-album')).to_have_class('screen on');expect(q.locator('#albSub')).to_contain_text('2026.10.29');assert q.evaluate("cur.eventEnd==='2026-10-29T23:59'")
 q.reload();q.locator('.album-tile').first.click();assert q.evaluate("cur.eventEnd==='2026-10-29T23:59'");q.locator('#albumAddFab').click();expect(q.locator('#s-options .photo-period-value')).to_contain_text('2026.10.29')
 assert not errors,errors
 checks=['Album creation stores meeting dates','Album info says meeting period','Upload defaults to meeting dates','Upload range independently editable','Import retains selected upload range','Completed upload preserves meeting dates','Reload preserves meeting dates','Next upload defaults to meeting dates']
 (out/'results.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},ensure_ascii=False,indent=2));print('PASS',len(checks),'meeting/upload range checks; JS errors 0');b.close()
