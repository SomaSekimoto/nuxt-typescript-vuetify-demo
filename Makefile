publish:
	npm run build
	npm run generate
	amplify publish
push:
	amplify push
