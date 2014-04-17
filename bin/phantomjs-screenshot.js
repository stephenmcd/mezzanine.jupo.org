var page = require('webpage').create();
var args = require('system').args;

page.viewportSize = {width: 1280, height: 1024};
page.open(args[1], function() {
  page.render(args[2], {format: 'jpeg', quality: '95'});
  phantom.exit();
});
