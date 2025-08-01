import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")



# Configure the Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

PROMPT = """
Generate complete Kubernetes manifests for a {language} application with best practices.
Include the following manifests separated by '---':
1. Deployment
2. Service
3. Ingress (basic setup)

Application details:
- Language: {language}
- App Name: {app_name}
- Port: {port}
- Replicas: {replicas}

Please provide clean YAML manifests without explanation, separated by '---' between different manifest types.
Include proper labels, selectors, and follow Kubernetes best practices.
"""

def generate_kubernetes_manifests(language, app_name, port, replicas):
    response = model.generate_content(
        PROMPT.format(
            language=language,
            app_name=app_name,
            port=port,
            replicas=replicas
        )
    )
    return response.text

if __name__ == '__main__':
    language = input("Enter the programming language: ")
    app_name = input("Enter application name (default: my-app): ") or "my-app"
    port = input("Enter application port (default: 8080): ") or "8080"
    replicas = input("Enter number of replicas (default: 3): ") or "3"
    
    manifests = generate_kubernetes_manifests(language, app_name, port, replicas)
    print("\nGenerated Kubernetes Manifests:\n")
    print(manifests)