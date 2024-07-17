let slideIndex = 0;
showSlides();

// Next-previous control
function nextSlide() {
	slideIndex++;
	showSlides();
	timer = _timer; // reset timer
}

function prevSlide() {
	slideIndex--;
	showSlides();
	timer = _timer;
}

// Thumbnail image controlls
function currentSlide(n) {
	slideIndex = n - 1;
	showSlides();
	timer = _timer;
}

function showSlides() {
	let slides = document.querySelectorAll(".mySlides");
	let dots = document.querySelectorAll(".dots");

	if (slideIndex > slides.length - 1) slideIndex = 0;
	if (slideIndex < 0) slideIndex = slides.length - 1;

	// hide all slides
	slides.forEach((slide) => {
		slide.style.display = "none";
	});

	// show one slide base on index number
	slides[slideIndex].style.display = "block";

	dots.forEach((dot) => {
		dot.classList.remove("actives");
	});

	// dots[slideIndex].classList.add("actives");
}

// autoplay slides --------
let timer = 7; // sec
const _timer = timer;

// this function runs every 1 second
setInterval(() => {
	timer--;

	if (timer < 1) {
		nextSlide();
		timer = _timer; // reset timer
	}
}, 1000); // 1sec

// Initialize the map
function initMap() {
	// Get map link from data attribute
	var mapDiv = document.getElementById("map");
	var mapLink = mapDiv.getAttribute("data-maplink");

	// Extract latitude and longitude from the map link
	var location = mapLink.match(/[-+]?\d+\.\d+/g);
	var latLng = {
		lat: parseFloat(location[0]),
		lng: parseFloat(location[1]),
	};

	// Initialize map using HERE Maps API
	var platform = new H.service.Platform({
		apikey: "r1sKeICFfoaDx-2QT8lzzqOYlCQ9vErgqcPilluU8Yc",
	});
	var defaultLayers = platform.createDefaultLayers();
	var map = new H.Map(
		document.getElementById("map"),
		defaultLayers.vector.normal.map,
		{
			center: latLng,
			zoom: 14, // Adjust zoom level as needed
		}
	);

	// Add marker
	var marker = new H.map.Marker(latLng);
	map.addObject(marker);

	// Enable zoom control
	var ui = H.ui.UI.createDefault(map, defaultLayers);
	var zoomControl = new H.ui.ZoomControl({
		alignment: H.ui.Layout.Alignment.RIGHT_TOP,
	});
	ui.addControl("zoomControl", zoomControl);
}
// Load map when the page is loaded
window.onload = initMap;

//image file input handling
document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const form = document.getElementById('reviewFormAjax');
    let files = [];

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.classList.add('dragover');
    }

    function unhighlight() {
        dropArea.classList.remove('dragover');
    }

    dropArea.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFiles, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const newFiles = [...dt.files];
        handleNewFiles(newFiles);
    }

    function handleFiles(e) {
        const newFiles = [...e.target.files];
        handleNewFiles(newFiles);
    }

    function handleNewFiles(newFiles) {
        files = [...files, ...newFiles];
        updateImagePreviews();
        updateFileInput();
    }

    function updateImagePreviews() {
        imagePreviewContainer.innerHTML = '';
        files.forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const div = document.createElement('div');
                div.className = 'image-preview';
                div.innerHTML = `
                    <img src="${e.target.result}" alt="Image preview">
                    <span class="remove-image" data-index="${index}">×</span>
                `;
                imagePreviewContainer.appendChild(div);
            }
            reader.readAsDataURL(file);
        });
    }

    function updateFileInput() {
        const dataTransfer = new DataTransfer();
        files.forEach(file => {
            dataTransfer.items.add(file);
        });
        fileInput.files = dataTransfer.files;
    }

    imagePreviewContainer.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-image')) {
            const index = parseInt(e.target.dataset.index);
            files.splice(index, 1);
            updateImagePreviews();
            updateFileInput();
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Handle success (e.g., show a success message, redirect)
                window.location.href = data.redirect_url;
            } else {
                // Handle error (e.g., show error message)
                console.error(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});



//review section and dataset
document.addEventListener("DOMContentLoaded", function () {
    let dataset, testimonialsData;

    try {
        dataset = JSON.parse(JSON.parse(document.getElementById('rating-count-data').textContent));
    } catch (e) {
        console.error("Error parsing rating count data:", e);
        dataset = [];
    }

    try {
        testimonialsData = JSON.parse(JSON.parse(document.getElementById('review-details-data').textContent));
    } catch (e) {
        console.error("Error parsing review details data:", e);
        testimonialsData = [];
    }

    console.log("Dataset:", dataset);
    console.log("TestimonialsData:", testimonialsData);

    // Function to update ratings
    function updateRatings() {
        let totalReviews = 0;
        let totalRating = 0;
        let totalNumbers = 0;
        
        dataset.forEach(item => {
            totalNumbers += item.count;
        });
        
        // Create an array to hold the rating data in the correct order
        const orderedRatings = [
            { rating: 5, text: 'Excellent' },
            { rating: 4, text: 'Very good' },
            { rating: 3, text: 'Average' },
            { rating: 2, text: 'Poor' },
            { rating: 1, text: 'Terrible' }
        ];
        
        orderedRatings.forEach((orderItem, index) => {
            const item = dataset.find(d => d.rating === orderItem.rating);
            if (item) {
                totalReviews += item.count;
                totalRating += item.rating * item.count;
                
                // Update individual rating bars and counts
                const barWidth = (item.count / totalNumbers) * 100;
                const ratingType = document.querySelectorAll('.rating-type')[index];
                const barFill = document.querySelectorAll('.fill')[index];
                const count = document.querySelectorAll('.count')[index];
                
                if (ratingType) ratingType.textContent = orderItem.text;
                if (barFill) barFill.style.width = `${barWidth}%`;
                if (count) count.textContent = `${item.count}`;
            }
        });

        // Update total review count and average rating
        const averageRating = totalReviews === 0 ? 0 : (totalRating / totalReviews).toFixed(1);
        const score = document.querySelector('.score');
        const reviewCount = document.querySelector('.review-count');
        if (score) score.textContent = averageRating;
        if (reviewCount) reviewCount.textContent = `${totalReviews} reviews`;
    }

    // Function to dynamically generate testimonials
    function generateTestimonials() {
        const container = document.getElementById('testimonial-container');
        if (!container) return;

        // If there are no reviews
        if (testimonialsData.length === 0) {
            const noReviewsBox = document.createElement('div');
            noReviewsBox.classList.add('testimonial-box');

            const noReviewsMsg = document.createElement('div');
            noReviewsMsg.classList.add('client-comment');
            const p = document.createElement('p');
            p.textContent = 'No Reviews';
            noReviewsMsg.appendChild(p);

            noReviewsBox.appendChild(noReviewsMsg);
            container.appendChild(noReviewsBox);
            return;
        }

        testimonialsData.forEach(testimonial => {
            // Create testimonial box
            const testimonialBox = document.createElement('div');
            testimonialBox.classList.add('testimonial-box');

            // Top section
            const topSection = document.createElement('div');
            topSection.classList.add('box-top');

            // Profile
            const profile = document.createElement('div');
            profile.classList.add('profile');

            // Profile image
            const profileImg = document.createElement('div');
            profileImg.classList.add('profile-img');
            const img = document.createElement('img');
            img.src = testimonial.gender == 1 
                ? "https://bootdey.com/img/Content/avatar/avatar7.png"
                : "/static/images/female_user.avif";
            profileImg.appendChild(img);
            profile.appendChild(profileImg);

            // Name and username
            const nameUser = document.createElement('div');
            nameUser.classList.add('name-user');
            const strong = document.createElement('strong');
            strong.textContent = testimonial.name;
            const span = document.createElement('span');
            span.textContent = '@' + testimonial.user_name;
            nameUser.appendChild(strong);
            nameUser.appendChild(span);
            profile.appendChild(nameUser);
            topSection.appendChild(profile);

            // Reviews
            const reviews = document.createElement('div');
            reviews.classList.add('reviews');
            for (let i = 0; i < testimonial.rating; i++) {
                const star = document.createElement('i');
                star.classList.add('fas', 'fa-star');
                reviews.appendChild(star);
            }
            for (let i = testimonial.rating; i < 5; i++) {
                const star = document.createElement('i');
                star.classList.add('far', 'fa-star');
                reviews.appendChild(star);
            }
            topSection.appendChild(reviews);

            testimonialBox.appendChild(topSection);

            // Client comment
            const clientComment = document.createElement('div');
            clientComment.classList.add('client-comment');
            const p = document.createElement('p');
            p.textContent = testimonial.review_text;
            clientComment.appendChild(p);
            testimonialBox.appendChild(clientComment);

            container.appendChild(testimonialBox);
        });
    }

    // Call the functions initially
    generateTestimonials();
    updateRatings();

    // Rating stars code
    const ratingDivs = document.querySelectorAll(".rating_value");

    ratingDivs.forEach(function (ratingDiv) {
        let totalReviews = 0;
        let totalRating = 0;
        dataset.forEach(item => {
            totalReviews += item.count;
            totalRating += item.rating * item.count;
        });
        const ratingValue = totalReviews === 0 ? 0 : (totalRating / totalReviews).toFixed(1);
        console.log("rating----->", ratingValue);
        if (!isNaN(ratingValue)) {
            setRating(ratingDiv, ratingValue);
        }
    });

    function setRating(ratingDiv, value) {
        const percentage = (100 - 10 * 2 * value);
        const totalWidth = 107; // Total width of the .rating_value div
        console.log("percentage--------->", percentage);

        const lastStarWidth = totalWidth - totalWidth * (percentage / 100);
        console.log("lastwidth---------->", lastStarWidth);
        // Set width of the last star
        if (percentage > 0 && percentage <= 100) {
            ratingDiv.style.width = `${lastStarWidth}px`;
        }
    }

    // Favorite icon functionality
    const favoriteIcon = document.getElementById("favorite-icon");
    if (favoriteIcon) {
        const placeId = favoriteIcon.getAttribute("data-place-id");

        // Initial check to set favorite icon color
        getFavorites(placeId);

        // Add click event listener to favorite icon
        favoriteIcon.addEventListener("click", function () {
            toggleFavorite(placeId);
        });
    }

    // Function to toggle favorite status
    function toggleFavorite(placeId) {
        const url = favoriteIcon.style.color === "red" ? "/remove_favorite/" : "/add_favorite/";
        const csrftoken = document.cookie.match(/csrftoken=([^ ;]+)/)[1];

        // Send AJAX request to add or remove favorite
        $.ajax({
            url: url,
            method: "POST",
            headers: { "X-CSRFToken": csrftoken },
            data: { place_id: placeId },
            success: function (response) {
                // Toggle favorite icon color
                if (favoriteIcon.style.color === "red") {
                    favoriteIcon.style.color = "white";
                } else {
                    favoriteIcon.style.color = "red";
                }
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
                // Handle error if needed
            },
        });
    }

    // Function to get favorites and update favorite icon color
    function getFavorites(placeId) {
        // Send AJAX request to get user's favorite places
        $.ajax({
            url: "/get_user_favorites/",
            method: "GET",
            success: function (response) {
                console.log("Favorites response:", response);
                const userFavorites = response.userFavorites;
                console.log("User favorites:", userFavorites);
                console.log("Place ID:", placeId);
                // Check if the icon's place ID is in the user's favorites
                let isFavorite = false;
                for (const favoriteId of userFavorites) {
                    console.log("Favorite ID:", favoriteId);
                    if (String(favoriteId) === String(placeId)) {
                        isFavorite = true;
                        break;
                    }
                }
                if (isFavorite) {
                    favoriteIcon.style.color = "red";
                } else {
                    favoriteIcon.style.color = "white";
                }
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
                // Handle error if needed
            },
        });
    }
});