import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")



# Configure the Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

GITHUB_ACTIONS_PROMPT = """
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
- Node/Python/Java version: Use latest stable
- Include security scanning
- Use GitHub secrets for sensitive data
- Include proper caching for dependencies

Please provide clean YAML without explanation, ready to save as .github/workflows/ci-cd.yml
"""

GITLAB_CI_PROMPT = """
Generate a complete GitLab CI/CD pipeline for a {language} application with best practices.
Include the following stages:
1. build
2. test  
3. security
4. docker-build
5. deploy

Application details:
- Language: {language}
- App Name: {app_name}
- Include unit tests, security scanning, Docker build
- Use GitLab CI variables for configuration
- Include staging and production deployment
- Add proper caching and artifacts

Please provide clean YAML without explanation, ready to save as .gitlab-ci.yml
"""

JENKINS_PROMPT = """
Generate a complete Jenkins pipeline (Jenkinsfile) for a {language} application with best practices.
Include the following stages:
1. Checkout
2. Build
3. Test
4. Security Scan
5. Docker Build
6. Deploy

Application details:
- Language: {language}
- App Name: {app_name}
- Use declarative pipeline syntax
- Include proper error handling
- Add post-build actions
- Include Docker build and deployment

Please provide clean Groovy pipeline code without explanation, ready to save as Jenkinsfile
"""

def generate_cicd_pipeline(platform, language, app_name):
    if platform.lower() == "github":
        prompt = GITHUB_ACTIONS_PROMPT
    elif platform.lower() == "gitlab":
        prompt = GITLAB_CI_PROMPT
    elif platform.lower() == "jenkins":
        prompt = JENKINS_PROMPT
    else:
        return "Unsupported platform. Choose: github, gitlab, or jenkins"
    
    response = model.generate_content(
        prompt.format(language=language, app_name=app_name)
    )
    return response.text

def get_filename(platform):
    filenames = {
        "github": ".github/workflows/ci-cd.yml",
        "gitlab": ".gitlab-ci.yml", 
        "jenkins": "Jenkinsfile"
    }
    return filenames.get(platform.lower(), "ci-cd-pipeline.yml")

if __name__ == '__main__':
    print("🔄 CI/CD Pipeline Generator")
    print("Available platforms: GitHub, GitLab, Jenkins")
    print("-" * 40)
    
    platform = input("Enter CI/CD platform: ")
    language = input("Enter the programming language: ")
    app_name = input("Enter application name (default: my-app): ") or "my-app"
    
    print(f"\nGenerating {platform} CI/CD Pipeline...")
    
    pipeline = generate_cicd_pipeline(platform, language, app_name)
    print(f"\nGenerated {platform} CI/CD Pipeline:\n")
    print(pipeline)
    
    filename = get_filename(platform)
    print(f"\n💡 Save this as: {filename}")