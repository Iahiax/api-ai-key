import os
from google.cloud import secretmanager

class KeyManager:
    """خزينة مركزية لإدارة وجلب مفاتيح الـ API لجميع النماذج والشركات المعتمدة"""
    
    def __init__(self, project_id):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id
        
        # القاموس الشامل لكل الشركات والخدمات التي ذكرتها
        self.secret_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GEMINI_API_KEY",
            "meta": "LLAMA_API_KEY",
            "microsoft": "AZURE_API_KEY",
            "xai": "GROK_API_KEY",
            "mistral": "MISTRAL_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "moonshot": "KIMI_API_KEY",
            "alibaba": "QWEN_API_KEY",
            "zhipu": "GLM_API_KEY",
            "ibm": "IBM_GRANITE_API_KEY",
            "dolphin": "DOLPHIN_API_KEY",
            "midjourney": "MIDJOURNEY_API_KEY",
            "stability": "STABILITY_API_KEY",
            "runway": "RUNWAY_API_KEY",
            "pika": "PIKA_API_KEY",
            "elevenlabs": "ELEVENLABS_API_KEY"
        }

    def get_api_key(self, provider):
        """جلب المفتاح السري من Google Secret Manager بناءً على اسم الشركة"""
        secret_id = self.secret_map.get(provider.lower())
        if not secret_id:
            raise ValueError(f"المزود {provider} غير مدرج في الخزينة المركزية.")
        
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
