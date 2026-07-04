# 🤖 Centralized AI Git Digest & Code Reviewer

An automated, cross-repository DevOps pipeline that leverages **Google Gemini AI** to monitor your project activities. It delivers structured **Daily Status Reports** or fully automated **Pull Request (PR) Code Reviews** straight to your Gmail inbox.

This setup is fully decentralized: your core Python processing engine stays securely inside your central repository, while your other project repositories seamlessly execute it using a small, 10-line pointer configuration without needing to clone or duplicate the source files.

---



1. **The Core Blueprint:** Your central repository holds the processing logic (`generate_digest.py`) and the primary workflow blueprint (`daily-update.yml`).
2. **The Trigger Pointer:** Any secondary project repository simply includes a lightweight YAML file pointing to your central workflow.
3. **Secure Computation:** GitHub Actions boots up a clean virtual cloud instance, maps the local repository data, extracts securely stored environment tokens, queries Gemini, sends the email, and completely wipes the session.

---

## ⚙️ Phase 1: Configuring Your Central Bot Repo

To allow other repositories to call your central script, your main automation repository must be open for communication.

### Scenario A: If Your Central Bot Repo is PUBLIC (Recommended)
No special settings are required! GitHub automatically permits external workflows to call reusable blueprints hosted inside public repositories. 
* *Note:* This is completely secure. Your secret API tokens and passwords are **never** committed to the codebase; they remain completely private inside your repository settings vault.

### Scenario B: If Your Central Bot Repo is PRIVATE and inside an Organization
If your central bot repository is private and belongs to a GitHub Organization (such as a school or team account), you must grant explicit cross-repo access:
1. Navigate to your central bot repository on GitHub.
2. Click **Settings** ➡️ **Actions** ➡️ **General**.
3. Scroll down to the **Access** section at the bottom of the page.
4. Select **"Accessible from repositories in the 'ORGANIZATION_NAME' organization"**.
5. Click **Save**.

---

## 🚀 Phase 2: Deploying to Other Repositories

Follow these steps for **every new repository** you want this AI assistant to monitor and review.

### Step 1: Add the Environment Secrets
Because GitHub keeps project environments strictly isolated for security, your secondary repository needs access to its own encrypted authentication tokens to talk to Gemini and Gmail.

1. Go to your new project repository page on GitHub.
2. Click **Settings** ➡️ **Secrets and variables** (on the left menu) ➡️ **Actions**.
3. Click the **New repository secret** button in the top right.
4. Add the following three keys exactly:

| Secret Key Name | What to Paste Into the Value Box |
| :--- | :--- |
| `GEMINI_API_KEY` | Your official Google Gemini API Developer Token. |
| `GMAIL_USERNAME` | Your full Gmail address (e.g., `yourname@gmail.com`). |
| `GMAIL_APP_PASSWORD` | The secure 16-character Google App Password (not your normal login password). |

### Step 2: Create the Workflow Folder Structure
In the root directory of your project code, create the standard hidden folder path required by GitHub Actions:
```bash
mkdir -p .github/workflows

---

### Step 3: Create the Trigger Pointer File
Inside that newly created .github/workflows/ folder, create a new file named run-bot.yml and paste the following 10-line configuration block:

yaml```
name:  Trigger Central AI Bot

on:
  push:
    branches: [ main ]
  pull_request:
    types: [ opened, synchronize ]

jobs:
  call-central-pipeline:
    # Change username and repository name below to point directly to your main central bot workflow
    uses: YOUR_GITHUB_USERNAME/YOUR_CENTRAL_REPO_NAME/.github/workflows/daily-update.yml@main
    secrets:
      GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
      GMAIL_USERNAME: ${{ secrets.GMAIL_USERNAME }}
      GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
      yaml```


  ⚠️ CRITICAL EDITS: Make sure to replace YOUR_GITHUB_USERNAME/YOUR_CENTRAL_REPO_NAME with your actual GitHub account username and the exact repository name where your central script is hosted. Keep the .github/workflows/daily-update.yml@main path intact

  Phase 3: How to Use and Test the System
Once your files are saved and pushed to your repository, the automation handles everything completely behind the scenes.

1. Automated Daily Status Report
How it triggers: It runs completely automatically every morning at your designated schedule (e.g., 5:42 AM PHT).

What it does: The pipeline wakes up, analyzes all git commit modifications pushed within the last 24 hours, queries Gemini for an architectural summary, and emails a clean "📊 Project Status Report" to your inbox so it's ready when you wake up.

2. Manual On-Demand Updates
How it triggers: Go to any active Issue thread or Pull Request page inside your GitHub repository and type the comment command: /update.

What it does: GitHub instantly overrides the standard timers, forces the cloud runner to spin up on-demand, compiles your repository status, and dispatches an analytical update directly to your email within seconds.

🛠️ Verification Checklist
If your automation fails to trigger, quickly double-check these settings:

[ ] Under Settings ➡️ Actions ➡️ General, verify that "Allow all actions and reusable workflows" is checked.
[ ] Under Settings ➡️ Actions ➡️ General (scroll to the bottom), ensure Workflow permissions is set to "Read and write permissions" so the runner can save text files.
[ ] Verify that your repository secrets match the variable names (GEMINI_API_KEY, GMAIL_USERNAME, GMAIL_APP_PASSWORD) with no accidental trailing spaces.