var Metalsmith = require('metalsmith');
var layouts = require('metalsmith-layouts');
var markdown = require('metalsmith-markdown');
var debug = require('metalsmith-debug');
var ignore = require('metalsmith-ignore');
var assets = require('metalsmith-assets');
var ancestry = require('metalsmith-ancestry');
var links = require('metalsmith-relative-links');
var paths = require('metalsmith-paths');

Metalsmith(__dirname)
    .use(ignore('**/*~'))
    .source('src')
    .destination('build')
    .clean(true)
    .use(paths())
    .use(ancestry())
    .use(links())
    .use(debug())
    .use(markdown())
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
