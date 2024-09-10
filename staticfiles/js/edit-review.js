document.addEventListener('DOMContentLoaded', function () {
    const ratingInput = document.getElementById('rating');
    const starRating = document.querySelector('.star-rating');
    const stars = starRating.querySelectorAll('.fa-star');
    const noRatingFeedback = document.getElementById('no-rating-feedback');

    function setInitialRating() {
        const currentRating = starRating.getAttribute('data-current-rating');
        if (currentRating) {
            ratingInput.value = currentRating;
            stars.forEach(star => {
                const starValue = star.getAttribute('data-value');
                if (starValue <= currentRating) {
                    star.classList.add('selected');
                }
            });
        }
    }

    /**
     * Handles the click event on a star.
     * Updates the rating input value and visually selects the stars up to the clicked star.
     */
    function handleStarClick() {
        const ratingValue = this.getAttribute('data-value');
        ratingInput.value = ratingValue;
        stars.forEach(s => s.classList.remove('selected'));
        this.classList.add('selected');
        let prev = this.previousElementSibling;
        while (prev) {
            prev.classList.add('selected');
            prev = prev.previousElementSibling;
        }
        noRatingFeedback.textContent = '';
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
     * Handles the mouseleave event on the star rating container.
     * Resets the visual highlight to the selected rating.
     */
    function handleStarMouseLeave() {
        stars.forEach(s => s.classList.remove('hovered'));
        const selectedRating = ratingInput.value;
        stars.forEach(star => {
            const starValue = star.getAttribute('data-value');
            if (starValue <= selectedRating) {
                star.classList.add('selected');
            } else {
                star.classList.remove('selected');
            }
        });
    }

    stars.forEach(star => {
        star.addEventListener('click', handleStarClick);
        star.addEventListener('mouseover', handleStarMouseOver);
    });

    starRating.addEventListener('mouseleave', handleStarMouseLeave);

    setInitialRating();
});