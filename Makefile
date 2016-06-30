html:
	env/bin/python build_pages.py

clean:
	rm -rf build

deploy:
	aws --profile manifestos.org.uk s3 sync build s3://manifestos.org.uk --delete
