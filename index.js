var Metalsmith = require('metalsmith');
var layouts = require('metalsmith-layouts');
var markdown = require('metalsmith-markdown');
var debug = require('metalsmith-debug');
var ignore = require('metalsmith-ignore');
var assets = require('metalsmith-assets');
var ancestry = require('metalsmith-ancestry');
var links = require('metalsmith-relative-links');
var paths = require('metalsmith-paths');
var handlebars = require('handlebars');
var cheerio = require('cheerio');
var repeatHelper = require('handlebars-helper-repeat');

handlebars.registerHelper('numbered_pages', function() {
    var $ = cheerio.load(this.contents);
    var nextPageNumber = 1;
    var path = "https://manifestos.org.uk" + this.path.href.replace(".md", ".html");
    var hashtags = this.hashtags
    $('a.page').each(function(i, elem) {
	var id = $(elem).attr("id");
	if (id == null) {
	    var number = nextPageNumber++;
	    id = "page-" + number;
	    $(this).attr("id", id);
	    $(this).text("Page " + number);
	} else if (id.startsWith("page-")) {
	    nextPageNumber++;
	}
	var anchorName = "#" + id;
	$(this).attr("href", anchorName);
	var parent = $(this).parent();
	var pageName = $(this).text();
	var url = "https://twitter.com/intent/tweet?url=" + encodeURI(path + anchorName) + "&via=uk_manifestos";
	parent.addClass("page-anchor-container");
	parent.append(" &ndash; <a class=\"view-original\" href=\"" + anchorName + "-original\">View original</a>");
	parent.append(" &ndash; <a class=\"share-twitter\" href=\"" + url + "\">Tweet</a>");
    });
    return $.html();
});

handlebars.registerHelper('uriencode', function(str) {
    return encodeURI(str);
});

handlebars.registerHelper('repeat', repeatHelper);

Metalsmith(__dirname)
    .use(ignore('**/*~'))
    .source('src')
    .destination('build')
    .clean(true)
    .use(paths())
    .use(ancestry())
    .use(links())
    .use(markdown())
    .use(debug())
    .use(layouts({
	engine: 'handlebars',
	partials: 'partials'
    }))
    .use(assets({
	source: './assets',
	destination: './assets'
    }))
    .build(function(err) {
	if (err) throw err;
    });
