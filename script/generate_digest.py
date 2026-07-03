import os
import subprocess
from google import genai

def get_git_log():
    """Extracts all commit messages from the past 24 hours."""
    try:
        # Runs git log command targeting modifications over the last 1 day
        result = subprocess.run(
            ["git", "log", "--since=24.hours", "--oneline"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error retrieving git changes: {str(e)}"

def main():
    # 1. Grab git changes
    git_history = get_git_log()
    
    if not git_history:
        summary_content = "No code updates or commits were pushed to the repository in the last 24 hours."
    else:
        # 2. Connect to Gemini API Client using the new google-genai SDK syntax
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        
        prompt = f"""
        You are a senior technical project supervisor. Review the following raw list of code commits pushed to this repository over the last 24 hours:
        
        {git_history}
        
        Provide a clean, bulleted daily summary of what features were built, what bugs were resolved, and a brief overall structural health evaluation of the project development velocity today. Keep it concise, professional, and engineering-focused.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        summary_content = response.text

    # 3. Write output to a clean file for the email builder stage
    with open("digest_output.txt", "w", encoding="utf-8") as f:
        f.write(summary_content)
    print("Success: digest_output.txt written successfully.")

if __name__ == "__main__":
    main()