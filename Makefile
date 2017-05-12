build: index.js node_modules $(shell find src layouts assets)
	node $<
	touch $@

node_modules: package.json
	npm install

clean:
	rm -rf build

deploy:
	aws --profile manifestos.org.uk s3 sync build s3://manifestos.org.uk --delete

.PHONY: clean deploy
