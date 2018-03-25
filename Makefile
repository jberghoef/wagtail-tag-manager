frontend:
	yarn build

watch:
	yarn dev
	yarn watch

git-reset:
	rm -rf .git
	git init
	git add .
	git commit -m "first commit"
	git remote add origin https://github.com/jberghoef/wagtail-tag-manager.git
	git push -u origin master --force
