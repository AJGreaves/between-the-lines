document.addEventListener('DOMContentLoaded', function () {

    const toggleReviewElements = document.querySelectorAll('.toggle-review');
    const stars = document.querySelectorAll('.star-rating .fa-star');
    const ratingInput = document.getElementById('rating');
    const reviewForm = document.getElementById('review-form');
    const ratingFeedbackElm = document.getElementById('no-rating-feedback');
    const deleteButton = document.getElementById('delete-review-btn');

    /**
     * Toggles between the short and full review of the relevant book.
     * The text content of the clicked element is also updated accordingly.
     * @param {Event} e - The click event.
     */
    function toggleReview(e) {
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
    }

    /**
     * Handles the click event on a star.
     * Updates the rating input value and visually selects 
     * the stars up to the clicked star.
     */
    function handleStarClick() {
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
    }

    /**
     * Handles the mouseover event on a star.
     * Visually highlights the stars up to the hovered star.
     */
    function handleStarMouseOver() {
        stars.forEach(s => s.classList.remove('hovered'));
        this.classList.add('hovered');
        let prev = this.previousElementSibling;
        while (prev) {
            prev.classList.add('hovered');
            prev = prev.previousElementSibling;
        }
    }

    /**
     * Handles the mouseout event on a star.
     * Removes the hover effect from all stars.
     */
    function handleStarMouseOut() {
        stars.forEach(s => s.classList.remove('hovered'));
    }

    /**
     * Validates the review form submission.
     * Prevents submission if no rating is selected and displays feedback.
     * @param {Event} e - The submit event.
     */
    function validateReviewForm(e) {
        if (!ratingInput.value) {
            e.preventDefault();
            ratingFeedbackElm.innerText = 'Please select a rating';
        }
    }

    /**
     * Handles the click event on the delete button.
     * Confirms the deletion and redirects to the delete review URL if confirmed.
     * @param {Event} event - The click event.
     */
    function handleDeleteClick(event) {
        event.preventDefault();
        const reviewId = this.getAttribute('data-review-id');
        const confirmDelete = confirm('Are you sure you want to delete this review?');

        if (confirmDelete) {
            // Redirect to the delete review URL
            window.location.href = `/reviews/delete_review/${reviewId}/`;
        }
    }

    toggleReviewElements.forEach(function (element) {
        element.addEventListener('click', toggleReview);
    });

    stars.forEach(star => {
        star.addEventListener('click', handleStarClick);
        star.addEventListener('mouseover', handleStarMouseOver);
        star.addEventListener('mouseout', handleStarMouseOut);
    });

    if (reviewForm) {
        reviewForm.addEventListener('submit', validateReviewForm);
    }

    if (deleteButton) {
        deleteButton.addEventListener('click', handleDeleteClick);
    }
});