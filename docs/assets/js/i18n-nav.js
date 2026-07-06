// i18n-nav-fix.js
// When on Chinese pages, rewrite nav links to stay on Chinese site
(function() {
    'use strict';
    
    // Only run on Chinese pages
    if (!window.location.pathname.includes('/zh/')) return;
    
    function rewriteNavLinks() {
        // Target both sidebar nav and top tabs
        var selectors = '.md-nav__link, .md-tabs__link';
        document.querySelectorAll(selectors).forEach(function(link) {
            var href = link.getAttribute('href');
            if (!href) return;
            
            // Skip external links, anchors, already-zh links
            if (href.startsWith('http') || href.startsWith('#') || href.includes('/zh/')) return;
            
            // Skip language switcher
            if (link.closest('.md-select__inner')) return;
            
            // For relative links like "../foundations/algorithm/", insert "zh/"
            // "../" from /zh/page goes to root, so "../zh/" goes to /zh/
            if (href.startsWith('../')) {
                var newHref = href.replace('../', '../zh/');
                link.setAttribute('href', newHref);
            }
        });
    }
    
    // Run on initial load
    rewriteNavLinks();
    
    // Re-run after instant navigation (Material's document$ observable)
    if (typeof document$ !== 'undefined' && document$.subscribe) {
        document$.subscribe(function() {
            rewriteNavLinks();
        });
    }
})();
