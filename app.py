import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


# Set your Gemini API key
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

DOCKER_PROMPT = """
Generate an ideal Dockerfile for {language} with best practices. Just share the Dockerfile without any explanation between two lines to make copying easy.
Include:
- Base image
- Installing dependencies
- Setting working directory
- Adding source code
- Running the application
"""

KUBERNETES_PROMPT = """
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

CICD_PROMPTS = {
    "GitHub Actions": """
Generate a complete GitHub Actions workflow for a {language} application with best practices.
Include the following stages:
1. Checkout code
2. Setup environment ({language})
3. Install dependencies
4. Run tests
5. Build application
6. Build and push Docker image
7. Deploy to staging/production

Application details:
- Language: {language}
- App Name: {app_name}
- Include security scanning and proper caching
- Use GitHub secrets for sensitive data

Please provide clean YAML without explanation, ready to save as .github/workflows/ci-cd.yml
""",
    "GitLab CI": """
Generate a complete GitLab CI/CD pipeline for a {language} application with best practices.
Include stages: build, test, security, docker-build, deploy

Application details:
- Language: {language}
- App Name: {app_name}
- Include unit tests, security scanning, Docker build
- Use GitLab CI variables for configuration

Please provide clean YAML without explanation, ready to save as .gitlab-ci.yml
""",
    "Jenkins": """
Generate a complete Jenkins pipeline (Jenkinsfile) for a {language} application with best practices.
Include stages: Checkout, Build, Test, Security Scan, Docker Build, Deploy

Application details:
- Language: {language}
- App Name: {app_name}
- Use declarative pipeline syntax with proper error handling

Please provide clean Groovy pipeline code without explanation, ready to save as Jenkinsfile
"""
}

def generate_dockerfile(language):
    response = model.generate_content(DOCKER_PROMPT.format(language=language))
    return response.text

def generate_kubernetes_manifests(language, app_name, port, replicas):
    response = model.generate_content(
        KUBERNETES_PROMPT.format(
            language=language,
            app_name=app_name,
            port=port,
            replicas=replicas
        )
    )
    return response.text

def generate_cicd_pipeline(platform, language, app_name):
    prompt = CICD_PROMPTS[platform]
    response = model.generate_content(
        prompt.format(language=language, app_name=app_name)
    )
    return response.text

def get_file_extension(platform):
    extensions = {
        "GitHub Actions": "yml",
        "GitLab CI": "yml",
        "Jenkins": "groovy"
    }
    return extensions[platform]

st.set_page_config(page_title="AI DevOps Generator", page_icon="🚀")
st.title("🚀 AI Assisted DevOps Generator")

tool = st.sidebar.selectbox(
    "Select Tool:",
    ["🐳 Docker Generator", "☸️ Kubernetes Generator", "🔄 CI/CD Generator"]
)

if tool == "🐳 Docker Generator":
    st.header("🐳 Docker Generator")
    
    language = st.text_input("Enter the programming language:")
    
    if st.button("Generate Dockerfile") and language.strip():
        with st.spinner("Generating Dockerfile..."):
            try:
                dockerfile = generate_dockerfile(language)
                st.subheader("📄 Generated Dockerfile")
                st.code(dockerfile, language="dockerfile")
            except Exception as e:
                st.error(f"Error: {e}")

elif tool == "☸️ Kubernetes Generator":
    st.header("☸️ Kubernetes Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.text_input("Programming Language:")
        app_name = st.text_input("Application Name:", value="my-app")
    
    with col2:
        port = st.number_input("Application Port:", min_value=1, max_value=65535, value=8080)
        replicas = st.number_input("Number of Replicas:", min_value=1, max_value=10, value=3)
    
    if st.button("Generate Kubernetes Manifests") and language.strip():
        with st.spinner("Generating Kubernetes manifests..."):
            try:
                manifests = generate_kubernetes_manifests(language, app_name, port, replicas)
                st.subheader("📄 Generated Kubernetes Manifests")
                st.code(manifests, language="yaml")
            except Exception as e:
                st.error(f"Error: {e}")

elif tool == "🔄 CI/CD Generator":
    st.header("🔄 CI/CD Pipeline Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "CI/CD Platform:",
            ["GitHub Actions", "GitLab CI", "Jenkins"]
        )
        language = st.text_input("Programming Language:", key="cicd_lang")
    
    with col2:
        app_name = st.text_input("Application Name:", value="my-app", key="cicd_app")
        
        filenames = {
            "GitHub Actions": ".github/workflows/ci-cd.yml",
            "GitLab CI": ".gitlab-ci.yml",
            "Jenkins": "Jenkinsfile"
        }
        st.info(f"📁 Save as: `{filenames[platform]}`")
    
    if st.button("Generate CI/CD Pipeline") and language.strip():
        with st.spinner(f"Generating {platform} pipeline..."):
            try:
                pipeline = generate_cicd_pipeline(platform, language, app_name)
                st.subheader(f"📄 Generated {platform} Pipeline")
                
                code_language = "yaml" if platform != "Jenkins" else "groovy"
                st.code(pipeline, language=code_language)
                
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.markdown("**🤖 Powered by Google Gemini AI**")