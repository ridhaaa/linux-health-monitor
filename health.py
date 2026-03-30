import urllib.request
import json
import subprocess

api_key = "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"
url = "https://api.groq.com/openai/v1/chat/completions"

output = { 'disk' : subprocess.run( ['df', '-h'], capture_output = True, text = True),
                'memory' : subprocess.run( ['free', '-h'], capture_output = True, text = True),
                'ports' : subprocess.run( ['ss', '-tlnp'], capture_output = True, text = True), 
                'failed' : subprocess.run( ['systemctl', '--failed'], capture_output = True, text = True), 
                'logins' : subprocess.run( ['last', '-10'], capture_output = True, text = True), 
                'logs' : subprocess.run( ['tail', '/var/log/syslog'], capture_output = True, text = True) }
report = (
    "=== DISK ===\n" + output['disk'].stdout +
    "\n=== MEMORY ===\n" + output['memory'].stdout +
    "\n=== PORTS ===\n" + output['ports'].stdout +
    "\n=== FAILED SERVICES ===\n" + output['failed'].stdout +
    "\n=== RECENT LOGINS ===\n" + output['logins'].stdout +
    "\n=== RECENT LOGS ===\n" + output['logs'].stdout
)

data = json.dumps({
	"model": "llama-3.1-8b-instant",
	"messages" : [
	{
		"role": "user",
		"content": f"Analyze this Linux system health data and give me a summary:\n\n{report}"
	}]
}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {api_key}","Content-Type": "application/json","User-Agent": "python-urllib/3.12" })
with urllib.request.urlopen(req) as response:
	result = json.loads(response.read().decode())
	print(result['choices'][0]['message']['content'])

