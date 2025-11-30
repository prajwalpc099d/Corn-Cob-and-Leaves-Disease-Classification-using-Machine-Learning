# GitHub Setup Instructions

✅ **Your project is ready to push!** Git LFS is already configured for large model files.

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `corn-disease-classification` (or your preferred name)
   - **Description**: "Flask web application for corn disease classification using multiple deep learning models"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 2: Push Your Code

After creating the repository, run these commands:

```bash
cd /Users/prajwalkulkarni/Desktop/GUI
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

## Alternative: Using SSH (if you have SSH keys set up)

```bash
cd /Users/prajwalkulkarni/Desktop/GUI
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## ✅ Git LFS Already Configured

Your project is already set up with Git LFS (Large File Storage) to handle the large model files:
- ✅ Git LFS installed and initialized
- ✅ All `.h5` files (10 model files) are tracked by Git LFS
- ✅ Files range from 11MB to 130MB each
- ✅ Total repository size: ~700MB

**Note:** When you push, Git LFS will upload the model files to GitHub's LFS storage. This may take a few minutes due to file sizes.

## Verify Your Push

After pushing:
1. Visit your repository on GitHub
2. Check that all files are present
3. Model files should show "Stored with Git LFS" badge
4. Verify the `.gitattributes` file is present (confirms LFS tracking)

## Troubleshooting

### If push fails due to authentication:
- Use a Personal Access Token instead of password
- Or set up SSH keys for easier authentication

### If LFS files don't upload:
- Ensure you have Git LFS installed: `git lfs version`
- Re-initialize: `git lfs install`
- Check tracking: `git lfs ls-files`

