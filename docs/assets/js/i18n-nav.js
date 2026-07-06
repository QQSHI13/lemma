// i18n-nav-fix.js
// When on Chinese pages, rewrite nav links to stay on Chinese site
(function() {
    'use strict';
    
    var path = window.location.pathname;
    // Check if we're on a Chinese page or a 404 served at a Chinese URL
    var isChinese = path.includes('/zh/') || path === '/zh' || path.startsWith('/zh/');
    
    if (!isChinese) return;
    
    function rewriteNavLinks() {
        var selectors = '.md-nav__link, .md-tabs__link, a.md-logo';
        document.querySelectorAll(selectors).forEach(function(link) {
            var href = link.getAttribute('href');
            if (!href) return;
            
            // Skip external links, anchors, already-zh links
            if (href.startsWith('http') || href.startsWith('#') || href.includes('/zh/')) return;
            
            // Skip language switcher
            if (link.closest('.md-select__inner')) return;
            
            // Handle absolute paths (on 404 page)
            if (href.startsWith('/')) {
                if (href === '/') {
                    link.setAttribute('href', '/zh/');
                } else {
                    link.setAttribute('href', '/zh' + href);
                }
                return;
            }
            
            // Handle relative paths like ".." or "../"
            if (href === '..' || href === '../') {
                link.setAttribute('href', './');
                return;
            }
            
            // For relative links like "../foundations/algorithm/", insert "zh/"
            if (href.startsWith('../')) {
                link.setAttribute('href', href.replace('../', '../zh/'));
            }
        });
    }
    
    // Run on initial load
    rewriteNavLinks();
    
    // Re-run after instant navigation (Material's document$ observable)
    if (typeof document$ !== 'undefined' && document$.subscribe) {
        document$.subscribe(function() { rewriteNavLinks(); });
    }
})();
