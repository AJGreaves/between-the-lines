
document.addEventListener('DOMContentLoaded', function () {

    /**
    * Adds event listeners to all elements with the class "toggle-review".
    * Toggles between the short and full review of the relevant book.
    * The text content of the clicked element is also updated accordingly. */
    const toggleReviewElements = document.querySelectorAll('.toggle-review');
    const stars = document.querySelectorAll('.star-rating .fa-star');
    const ratingInput = document.getElementById('rating');
    const reviewForm = document.getElementById('review-form');
    const ratingFeedbackElm = document.getElementById('no-rating-feedback');

    toggleReviewElements.forEach(function (element) {
        element.addEventListener('click', function (e) {
            e.preventDefault();
            const fullReview = this.previousElementSibling;
            const shortReview = fullReview.previousElementSibling;

            if (fullReview.style.display === 'none') {
                shortReview.style.display = 'none';
                fullReview.style.display = 'block';
                this.textContent = 'Read less';
            } else {
                fullReview.style.display = 'none';
                shortReview.style.display = 'block';
                this.textContent = 'Read more';
            }
        });
    });

    stars.forEach(star => {
        star.addEventListener('click', function () {
            const rating = this.getAttribute('data-value');
            ratingInput.value = rating;
            stars.forEach(s => s.classList.remove('selected'));
            this.classList.add('selected');
            let prev = this.previousElementSibling;
            while (prev) {
                prev.classList.add('selected');
                prev = prev.previousElementSibling;
            }
            ratingFeedbackElm.style.display = 'none';
        });

        star.addEventListener('mouseover', function () {
            stars.forEach(s => s.classList.remove('hovered'));
            this.classList.add('hovered');
            let prev = this.previousElementSibling;
            while (prev) {
                prev.classList.add('hovered');
                prev = prev.previousElementSibling;
            }
        });

        star.addEventListener('mouseout', function () {
            stars.forEach(s => s.classList.remove('hovered'));
        });
    });

    reviewForm.addEventListener('submit', function (e) {
        if (!ratingInput.value) {
            e.preventDefault();
            ratingFeedbackElm.innerText = 'Please select a rating';
        }
    });
});