# Setup Instructions

## What's been done

✅ Created Python script to fetch download counts
✅ Created GitHub Actions workflow (runs daily at midnight UTC)
✅ Tested script - successfully found 68 models
✅ Initial CSV created with current download counts
✅ Git repository initialized with initial commit

## What you need to do

### 1. Create the private GitHub repository

Go to https://github.com/new and create a new **private** repository:
- Name: `vismatch-downloads-tracker` (or whatever you prefer)
- Visibility: **Private**
- Don't initialize with README, .gitignore, or license (we already have these)

### 2. Push the code

After creating the repo, GitHub will show you commands. Use these:

```bash
cd ~/vismatch-downloads-tracker
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/vismatch-downloads-tracker.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### 3. Verify it's working

1. Go to your repo on GitHub
2. Click the "Actions" tab
3. You should see the "Fetch Daily Download Counts" workflow
4. Click "Run workflow" to test it manually (don't wait for midnight!)
5. After it runs, check that `downloads.csv` was updated

### 4. That's it!

The workflow will now run automatically every day at 00:00 UTC. You can:
- View the Actions tab to see run history
- Download the CSV anytime to analyze data
- Make the repo public later if you want (Settings → Danger Zone → Change visibility)

## Troubleshooting

If the workflow fails:
- Check the Actions tab for error logs
- Make sure the repo has write permissions (it should by default)
- Try running manually first to debug

## Next steps (optional)

You could later add:
- A Python script to generate charts/graphs from the CSV
- GitHub Pages to display the data publicly
- Notifications if download counts spike
- Export to Google Sheets for easier visualization
