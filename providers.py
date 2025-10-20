import os, json, requests

class DummyProvider:
    name = "dummy"
    def __init__(self, model="local"): self.model = model
    def chat(self, prompt, history):
        last = history[-1] if history else ""
        return f"[NovaLocal] {prompt} (ctx:{last[:60]})"

class OpenAIProvider:
    name = "openai"
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY missing")
        self.url = "https://api.openai.com/v1/chat/completions"
    def chat(self, prompt, history):
        messages = [{"role":"system","content":"Tu es Nova, assistante IA utile et concise."}]
        for h in history[-6:]:
            messages.append({"role":"user","content":h})
        messages.append({"role":"user","content":prompt})
        r = requests.post(self.url,
            headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"},
            data=json.dumps({"model": self.model, "messages": messages, "temperature":0.3}),
            timeout=30
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()

def get_provider(name: str, model: str):
    name = (name or "dummy").lower()
    if name == "openai": return OpenAIProvider(model=model)
    return DummyProvider(model=model)
