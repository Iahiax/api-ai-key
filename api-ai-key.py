import os
from google.cloud import secretmanager

class KeyManager:
    """خزينة مركزية لإدارة وجلب مفاتيح الـ API للنماذج العالمية"""
    
    def __init__(self, project_id):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id

    def get_api_key(self, model_provider):
        """جلب المفتاح بناءً على اسم الشركة (المزود)"""
        # الخريطة البرمجية لأسماء المفاتيح في Google Secret Manager
        secret_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GEMINI_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "mistral": "MISTRAL_API_KEY",
            "xai": "GROK_API_KEY",
            "xai_grok": "GROK_API_KEY",
            "alibaba": "QWEN_API_KEY"
        }
        
        secret_id = secret_map.get(model_provider.lower())
        if not secret_id:
            raise ValueError(f"المفتاح الخاص بالمزود {model_provider} غير معرف في الخزينة.")
        
        # استدعاء من Google Cloud
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

# مثال على الاستخدام داخل الفريق:
# manager = KeyManager(project_id="my-project-id")
# openai_key = manager.get_api_key("openai")
