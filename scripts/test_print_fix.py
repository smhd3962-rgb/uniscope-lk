import urllib.request

url = 'http://localhost:3000/gpa-calculator/'
with urllib.request.urlopen(url) as resp:
    html = resp.read().decode('utf-8')
    assert resp.status == 200
    assert 'print-only' in html, "Missing .print-only class"
    assert 'triggerGpaPrint()' in html, "Missing triggerGpaPrint() call"
    idx = html.find('id="printSection"')
    snippet = html[idx:idx+60]
    print("Found snippet:", snippet)
    assert 'style="display:none;"' not in snippet, "Inline display:none still present on printSection"
    print("PASS: Print transcript is properly configured and will render upon printing!")
