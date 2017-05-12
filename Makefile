build: node_modules
	node index.js
	touch $@

node_modules: package.json
	npm install

clean:
	rm -rf build

deploy:
	aws --profile manifestos.org.uk s3 sync build s3://manifestos.org.uk --delete

.PHONY: build clean deploy
