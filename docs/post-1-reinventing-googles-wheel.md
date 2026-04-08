# Why I Spent Four Months Reinventing Google's Wheel

I spent four months building a Google Sheets-based system to manage permissions for a volunteer organization's Google Drive. The architecture was solid, the code worked, and I built a prompt-defined installation assistant on top of it. Then I discovered Google had already solved the problem.

### The Plausible Bad Idea

My goal was simple: help a small volunteer organization manage permissions for their Google Drive folders. Being new to Google's ecosystem, I designed what I thought was a clever, low-cost solution: using a Google Sheet as a central control panel to define user groups and manage access rights for free, personal Google accounts.

### The Power of Inertia

I soon discovered Google Workspace, which I realized was a better foundation. But instead of pivoting, I fell prey to inertia. Justified by supposed cost-savings and encouragement from the AI chatbots I consulted, I doubled down. I spent months writing extensive Apps Scripts to sync my Google Sheet with Google's backend.

The system worked, but it was a complex and brittle abstraction. Since my "Sheet Editors" weren't admins, syncs had to run on a delay. The solution created its own problems, requiring extensive auditing features just to keep it in check.

### The Unraveling

The breaking point was a feature request for multi-person approval on permission changes. As I tried to architect it, I realized my entire system was fighting against Google Drive's native behavior.

This forced me to finally look deeper at the tools I had been so busy replacing. That's when I discovered **Shared Drives**—Google's built-in model for team-owned content and access. For most organizations I was targeting, it covered the core need better than my custom layer.

### The Post-Mortem: My Critical Mistake

My biggest mistake wasn't technical; it was a failure of due diligence. **I never consulted a single professional in the field.** I relied on my own assumptions and an AI echo chamber. A chatbot is excellent at helping you solve the problem you present, but it won't tell you you're asking the wrong question.

### What Actually Came Out of It

So was it all a waste? No. While the project was a lesson in what not to build, the experience taught me invaluable lessons in professional growth and humility.

My decision rule now is simple: start with native Google Workspace/Drive capabilities first, and add automation only for narrow, recurring gaps.

Ironically, the most valuable artifact from this entire project wasn't the permission system, but the setup-assistant pattern that emerged from handling its complex installation. The principles I discovered there turned out to be more reusable than the original project. In the follow-up post, I describe how that pattern evolved into an open-source guided installation kit — one that anyone with an AI assistant and a terminal can use.
