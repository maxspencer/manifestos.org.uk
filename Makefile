html:
	mkdir -p build/includes
	env/bin/python build_pages.py
	cp -r includes/* build/includes

clean:
	rm -rf build

deploy:
	aws --profile manifestos.org.uk s3 sync build s3://manifestos.org.uk --delete
