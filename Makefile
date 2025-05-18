

clean:
	rm -rf _site

rebuild:
	rm -rf _site; bun eleventy

serve:
	rm -rf _site; bun eleventy --serve
