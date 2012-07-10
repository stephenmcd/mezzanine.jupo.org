$(function() {

    // Rotating quotes.
    var quoteInterval;
    var quotes = function() {
        quoteInterval = setInterval(function() {
            var current, next;
            $.each($('.quotes li'), function(i, quote) {
                quote = $(quote);
                if (!current && quote.is(':visible')) {
                    current = quote;
                } else if (current && !next) {
                    next = quote;
                }
            });
            if (!next) {
                next = $('.quotes li:first');
            }
            if (current) {
                current.fadeOut(200, function() {
                    next.fadeIn(200);
                });
            }
        }, 6000);
    };
    $('.quotes li').mouseover(function() {
        clearInterval(quoteInterval)
    });
    $('.quotes li').mouseover(quotes);
    quotes();

    // Sites carousel
    $('.carousel').mouseenter(function() {
        $(this).carousel('pause');
    }).mouseleave(function() {
        $(this).carousel('next');
    }).carousel();

    // Flattr button
    (function() {
        var s = document.createElement('script'), t = document.getElementsByTagName('script')[0];
        s.type = 'text/javascript';
        s.async = true;
        s.src = 'http://api.flattr.com/js/0.6/load.js?mode=auto';
        t.parentNode.insertBefore(s, t);
    })();

});

// Google analytics
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-52596-12']);
_gaq.push(['_trackPageview']);
(function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
