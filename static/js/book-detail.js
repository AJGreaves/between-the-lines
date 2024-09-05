/**
 * Adds event listeners to all elements with the class "toggle-review".
 * Toggles between the short and full review of the relevant book.
 * The text content of the clicked element is also updated accordingly. */
$(document).ready(function() {
    $('.toggle-review').on('click', function(e) {
        e.preventDefault();
        const $fullReview = $(this).prev('.full-review');
        const $shortReview = $fullReview.prev('.short-review');
        
        if ($fullReview.is(':hidden')) {
            $shortReview.hide();
            $fullReview.slideDown('medium');
            $(this).text('Read less');
        } else {
            $fullReview.hide();
            $shortReview.fadeIn('medium');
            $(this).text('Read more');
        }
    });
});