from wps_sdk import WPSClient

client = WPSClient(api_key="SX20251113HXLMYW",api_secret="jVSbQeGbpmBNsAFibSEaAFdAwZuKoYWH")

content = "这是更新后的内容测试一下"
new_content=content
client.update_document(doc_id="cjpVZz0ASxGp",content=new_content)
