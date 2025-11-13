from wps_sdk import WPSClient

client = WPSClient(api_key="SX20251113HXLMYW",api_secret="jVSbQeGbpmBNsAFibSEaAFdAwZuKoYWH")
with open('README.md', 'r', encoding='utf-8') as f:
content = f.read()
new_content=content
client.update_document(doc_id="cjpVZz0ASxGp",content=new_content)
