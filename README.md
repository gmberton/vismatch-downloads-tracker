# VisMatch Download Tracker

Automatically tracks download counts for all models in the [vismatch](https://huggingface.co/vismatch) HuggingFace organization.

## How it works

- GitHub Actions runs daily at 00:00 UTC
- Fetches download counts for all vismatch models using the HuggingFace API
- Appends data to `downloads.csv` with date and counts for each model
- Automatically commits and pushes changes

## Files

- `fetch_downloads.py` - Python script that fetches download counts
- `.github/workflows/daily-fetch.yml` - GitHub Actions workflow (scheduled daily)
- `downloads.csv` - Historical download data (automatically created)
- `requirements.txt` - Python dependencies

## CSV Format

```csv
date,model1,model2,model3,...
2024-01-01,1000,500,750,...
2024-01-02,1050,520,780,...
```

- First column: Date (YYYY-MM-DD)
- Subsequent columns: Download count for each model
- New models are automatically added as new columns when detected

## Manual Run

You can manually trigger the workflow:
1. Go to the "Actions" tab
2. Select "Fetch Daily Download Counts"
3. Click "Run workflow"

## Local Testing

```bash
pip install -r requirements.txt
python fetch_downloads.py
```

This will create/update `downloads.csv` with the current download counts.
