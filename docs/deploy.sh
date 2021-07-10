#!/usr/bin/env sh

# abort on errors
set -e

# change directory to script location
initial_dir="$(pwd)"
cd "$(dirname "$0")"

# build
npm run build

# navigate into the build output directory
cd .vuepress/dist

# if you are deploying to a custom domain
# echo 'www.example.com' > CNAME

git init
git add -A
git commit -m 'deploy'

# if you are deploying to https://<USERNAME>.github.io
# git push -f git@github.com:<USERNAME>/<USERNAME>.github.io.git master

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:nobeam/latticejson.git master:gh-pages

cd initial_dir