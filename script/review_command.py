import os
from google import genai

def main():
    
    comment_body = os.environ.get("COMMENT_BODY", "").strip()
    
    
    parts = comment_body.split(maxsplit=1)
    
    if len(parts) < 2:
       
        with open("review_result.txt", "w", encoding="utf-8") as f:
            f.write(" **Usage Error:** Please specify a file path. Example: `/review james.py` or `/review folder/app.js`")
        return

    
    target_file = parts[1].strip()

   
    if not os.path.exists(target_file):
        with open("review_result.txt", "w", encoding="utf-8") as f:
            f.write(f" **Error:** Could not find the file `{target_file}` anywhere in the repository.")
        return

    print(f"Reading requested file: {target_file} for AI review...")
    with open(target_file, "r", encoding="utf-8") as f:
        file_content = f.read()

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    prompt = f"""
    You are an expert senior software engineer performing a code review requested via command interface.
    Analyze the file '{target_file}' rigorously.
    
    Provide actionable feedback broken into:
    -  **Logic & Runtime Bugs**: Highlight any crash conditions, edge cases, or logic flaws.
    -  **Clean Code & Optimization**: Suggestions for formatting, architectural cleanups, or optimizations.
    
    Source code content:
    ```
    {file_content}
    ```
    """
    
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt,
    )
    
    with open("review_result.txt", "w", encoding="utf-8") as f:
        f.write(f"###  AI Code Review for `{target_file}`\n\n" + response.text)

if __name__ == "__main__":
    main()