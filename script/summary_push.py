import os
import subprocess
from google import genai

def get_git_diff():
    # Grabs the changes made in the very last commit push
    result = subprocess.run(["git", "diff", "HEAD~1", "HEAD"], capture_output=True, text=True)
    return result.stdout

def clean_diff(diff_text):
    #
    filtered_lines = []
    skip_file = False
    for line in diff_text.split('\n'):
        if line.startswith('diff --git'):
            if any(x in line for x in ['package-lock.json', 'poetry.lock', '.png', '.jpg', 'node_modules']):
                skip_file = True
            else:
                skip_file = False
        if not skip_file:
            filtered_lines.append(line)
    return '\n'.join(filtered_lines)

def main():
    raw_diff = get_git_diff()
    clean_code = clean_diff(raw_diff)
    
    if not clean_code.strip():
        print("No meaningful source code changes detected.")
        return

   
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    prompt = (
        "You are an automated project bot. Summarize these code changes into a "
        "bulleted list for a project management tracking ticket:\n\n" + clean_code
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
    # Write the AI summary to a text file for GitHub Actions to read
    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    main()

    #ang pogi ko