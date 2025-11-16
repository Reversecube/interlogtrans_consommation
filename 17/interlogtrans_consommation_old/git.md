```Remove-Item -Recurse -Force .git
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin url
git pull origin main --allow-unrelated-histories
git push -u origin main
```