function editProfile() {
	$("#heading").text("Edit Profile");
	$("#editProfileModal").modal("show");
}
$(document).ready(function () {
	$("#editProfile").submit(function (event) {
		event.preventDefault();
		if (validateBus()) {
			this.submit();
		}
	});

	const showError = (message) => {
		const errorDisplay = $(".error");
		errorDisplay.text(message);
		errorDisplay
			.closest(".input-control")
			.addClass("error")
			.removeClass("success");
	};

	const showSuccess = () => {
		const errorDisplay = $(".error");
		errorDisplay.text("");
		errorDisplay
			.closest(".input-control")
			.addClass("success")
			.removeClass("error");
	};

	const validateBus = () => {
		const name = $("#name");
		const email = $("#email");
		const phone = $("#phone");
		const gender = $("#gender");
		const address = $("#address");

		if (name.val() == "") {
			showError("Name is required");
			return false;
		}
		if (email.val() === "") {
			showError("Email is required");
			return false;
		}
		if (phone.val() == "") {
			showError("Phone is required");
			return false;
		}
		if (gender.val() == "-1") {
			showError("Gender is required");
			return false;
		}
		if (address.val() == "") {
			showError("Address is required");
			return false;
		}

		showSuccess();
		return true;
	};
});
function editProfile() {
	$("#heading").text("Edit Profile");
	$("#editProfileModal").modal("show");
}
var styleElement = document.createElement("style");
document.head.appendChild(styleElement);

styleElement.textContent = `
		.rating {
			font-size: 24px;
			display: flex;
			align-items: center;
			width: 107px; /* Adjust the width as desired */
			height: 25px; /* Adjust the height as desired */
			overflow: hidden; /* Ensure overflow is hidden */
		}
		
		.star {
			color: #ffd700; /* Gold color */
			width: 20px;
		}
		
		.rating-value {
			font-size: 24px;
			margin-left: 110px;
			margin-bottom: 50px;
			float: right; /* Move to the right */
			font: 0.8em "roboto";
			font-weight: bold;
		}
	`;

const generateRating = (ratingDiv, value) => {
	const percentage = 100 - 10 * 2 * value; // Total number of stars
	const totalWidth = 107; // Total width of the .rating div
	console.log("percentage   ajax.js --------->", percentage);

	const lastStarWidth = totalWidth - totalWidth * (percentage / 100);
	console.log("lastwidth---------->", lastStarWidth);
	// Set width of the last star
	if (percentage > 0 && percentage <= 100) {
		ratingDiv.style.width = `${lastStarWidth}px`;
	}
};

document.addEventListener("DOMContentLoaded", function () {
	const ratingDivs = document.querySelectorAll(".rating");

	ratingDivs.forEach(function (ratingDiv) {
		const ratingValue = parseFloat(ratingDiv.getAttribute("data-rating"));
		if (!isNaN(ratingValue)) {
			generateRating(ratingDiv, ratingValue);
		}
	});
});

$(document).ready(function () {
	var values = [];

	// Function to handle checkbox change
	function handleCheckboxChange() {
		var value = $(this).val();

		if ($(this).is(":checked")) {
			values.push(value);
			console.log("added", value);
			console.log(values);
		} else {
			var index = values.indexOf(value);
			if (index !== -1) {
				values.splice(index, 1);
			}
		}
	}

	// Attach change event listener to checkboxes
	$(".form-check-input").change(handleCheckboxChange);

	// Rest of your code here...
	$("#selectButton").click(function (event) {
		event.preventDefault(); // Prevent default form submission

		if (values.length > 0) {
			$.ajax({
				url: "/preferences/",
				method: "POST",
				data: { values: values },
				success: function (response) {
					console.log(response);
					const heading = document.querySelector("#recHeading");
					heading.innerHTML = "Places";
					const row = document.querySelector("#recommand");
					if (row) {
						row.innerHTML = "";

						response.forEach(function (item) {
							const colDiv = document.createElement("div");
							colDiv.classList.add("article");

							// Create article element with class 'article'
							const article = document.createElement("article");
							//article.classList.add("article");

							// Create figure element
							const figure = document.createElement("figure");

							// Create img element
							const img = document.createElement("img");
							img.setAttribute(
								"src",
								`../static/images/place_image/${item.ID}/${item.ID}a.jpg`
							);
							img.setAttribute("alt", "...");
							img.classList.add("card-img-top");
							img.setAttribute("height", "250px");
							img.setAttribute("width", "100%");

							// Append img to figure
							figure.appendChild(img);

							// Create favorite icon element
							const favoriteIcon =
								createFavoriteIconAndHandleFavorites(item.ID);

							// Append favorite icon to figure
							figure.append(favoriteIcon);

							// Create div element with class 'article-body'
							const articleBodyDiv =
								document.createElement("div");
							articleBodyDiv.classList.add("article-body");

							// Create h6 element with class 'card-title'
							const cardTitle = document.createElement("h6");
							cardTitle.textContent = item.Name; // Set the title from the object

							// Generate rating

							// Create p element with class 'card-text description'
							const cardText = document.createElement("p");
							cardText.classList.add("card-text", "description");
							cardText.textContent =
								item.Description.substring(0, 250) + "..."; // Set truncated description from the object

							// Create div element with class 'description-container'
							const descriptionContainerDiv =
								document.createElement("div");
							descriptionContainerDiv.classList.add(
								"description-container"
							);

							const ratingandbutton =
								document.createElement("div");
							ratingandbutton.classList.add("rating-and-button");

							const ratingandtext = document.createElement("div");
							ratingandtext.classList.add("rating-and-text");

							// Generate rating
							const ratingDiv = document.createElement("div");
							ratingDiv.classList.add("rating");
							ratingDiv.innerHTML = `
					<span class="star">&#9733;</span>
					<span class="star">&#9733;</span>
					<span class="star">&#9733;</span>
					<span class="star">&#9733;</span>
					<span class="star">&#9733;</span>
					`;
							generateRating(ratingDiv, item.Ratings);

							// Create rating value div
							const ratingValueDiv =
								document.createElement("div");
							ratingValueDiv.classList.add("rating-text");
							ratingValueDiv.innerHTML = `
						<span class="rating-valuee">${item.Ratings}/5</span>
                        
					`;
							const buttonlink = document.createElement("div");
							buttonlink.classList.add("button-link");
							buttonlink.innerHTML = `<a href="${item.Map_link}" class="redirect-button"></a>`;
							ratingandtext.appendChild(ratingDiv);
							ratingandtext.appendChild(ratingValueDiv);
							ratingandbutton.appendChild(ratingandtext);
							ratingandbutton.appendChild(buttonlink);

							descriptionContainerDiv.appendChild(
								ratingandbutton
							);

							// Append cardText to descriptionContainerDiv
							descriptionContainerDiv.appendChild(cardText);

							// Append elements to each other
							articleBodyDiv.appendChild(cardTitle);
							articleBodyDiv.appendChild(descriptionContainerDiv);
							article.appendChild(figure);
							article.appendChild(articleBodyDiv);
							colDiv.appendChild(article);

							row.appendChild(colDiv);

							// Create anchor element with class 'read-more'
							const readMoreLink = document.createElement("a");
							readMoreLink.setAttribute(
								"href",
								`/getMoreDetails/${item.ID}/`
							);
							readMoreLink.classList.add("read-more");
							readMoreLink.textContent = "Read More";

							// Create span element with class 'sr-only'
							const srOnlySpan = document.createElement("span");
							srOnlySpan.classList.add("sr-only");
							srOnlySpan.textContent = "about this is some title";

							// Create svg element with class 'icon'
							const svgIcon = document.createElementNS(
								"https://www.w3.org/2000/svg",
								"svg"
							);
							svgIcon.setAttribute(
								"xmlns",
								"https://www.w3.org/2000/svg"
							);
							svgIcon.classList.add("icon");
							svgIcon.setAttribute("viewBox", "0 0 20 20");
							svgIcon.setAttribute("fill", "currentColor");

							// Create path element inside svg
							const path = document.createElementNS(
								"https://www.w3.org/2000/svg",
								"path"
							);
							path.setAttribute("fill-rule", "evenodd");
							path.setAttribute(
								"d",
								"M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z"
							);
							path.setAttribute("clip-rule", "evenodd");

							// Append path to svg
							svgIcon.appendChild(path);

							// Append span and svg to anchor
							readMoreLink.appendChild(srOnlySpan);
							readMoreLink.appendChild(svgIcon);

							// Append anchor to article
							descriptionContainerDiv.appendChild(readMoreLink);
						});
					} else {
						console.error("Row element not found.");
					}
				},
				error: function (xhr, status, error) {
					console.error(xhr.responseText);
				},
			});
		} else {
			console.error("Values array is empty.");
		}
	});
});

function searchPlaces(query) {
	if (query.length >= 2) {
		fetch(`/search_places/?query=${query}`)
			.then((response) => response.json())
			.then((data) => {
				console.log(data);
				const row = document.querySelector("#row");
				row.innerHTML = "";
				data.forEach((item) => {
					const colDiv = document.createElement("div");
					colDiv.classList.add("article");

					// Create article element with class 'article'
					const article = document.createElement("article");
					//article.classList.add("article");

					// Create figure element
					const figure = document.createElement("figure");

					// Create img element
					const img = document.createElement("img");
					img.setAttribute(
						"src",
						`../static/images/place_image/${item.ID}/${item.ID}a.jpg`
					);
					img.setAttribute("alt", "...");
					img.classList.add("card-img-top"); // Remove 'img-fluid' class
					img.style.height = "100%"; // Set a fixed height for the image
					img.style.width = "100%"; // Ensure the width adjusts to the container

					// Append img to figure
					figure.appendChild(img);
					// Create favorite icon element
					const favoriteIcon = createFavoriteIconAndHandleFavorites(
						item.ID
					);

					// Append favorite icon to figure
					figure.appendChild(favoriteIcon);

					// Create div element with class 'article-body'
					const articleBodyDiv = document.createElement("div");
					articleBodyDiv.classList.add("article-body");

					// Create h6 element with class 'card-title'
					const cardTitle = document.createElement("h6");
					cardTitle.textContent = item.Name; // Set the title from the object

					// Append cardTitle to articleBodyDiv
					articleBodyDiv.appendChild(cardTitle);

					const descriptionContainerDiv =
						document.createElement("div");
					descriptionContainerDiv.classList.add(
						"description-container"
					);

					const ratingandbutton = document.createElement("div");
					ratingandbutton.classList.add("rating-and-button");

					const ratingandtext = document.createElement("div");
					ratingandtext.classList.add("rating-and-text");

					// Generate rating
					const ratingDiv = document.createElement("div");
					ratingDiv.classList.add("rating");
					ratingDiv.innerHTML = `
					<span class="star">&#9733;</span>
					<span class="star">&#9733;</span>
					<span class="star">&#9733;</span>
					<span class="star">&#9733;</span>
					<span class="star">&#9733;</span>
					`;
					generateRating(ratingDiv, item.Ratings);

					// Create rating value div
					const ratingValueDiv = document.createElement("div");
					ratingValueDiv.classList.add("rating-text");
					ratingValueDiv.innerHTML = `
						<span class="rating-valuee">${item.Ratings}/5</span>
                        
					`;
					const buttonlink = document.createElement("div");
					buttonlink.classList.add("button-link");
					buttonlink.innerHTML = `<a href="${item.Map_link}" class="redirect-button"></a>`;
					ratingandtext.appendChild(ratingDiv);
					ratingandtext.appendChild(ratingValueDiv);
					ratingandbutton.appendChild(ratingandtext);
					ratingandbutton.appendChild(buttonlink);

					descriptionContainerDiv.appendChild(ratingandbutton);

					// Create p element with class 'card-text description'
					const cardText = document.createElement("p");
					cardText.classList.add("card-text", "description");
					cardText.textContent =
						item.Description.substring(0, 250) + "..."; // Set truncated description from the object

					// Create div element with class 'description-container'

					// Append cardText to descriptionContainerDiv

					descriptionContainerDiv.appendChild(cardText);

					// Append elements to each other
					articleBodyDiv.appendChild(cardTitle);
					articleBodyDiv.appendChild(descriptionContainerDiv);
					article.appendChild(figure);
					article.appendChild(articleBodyDiv);
					colDiv.appendChild(article);

					row.appendChild(colDiv);

					// Create anchor element with class 'read-more'
					const readMoreLink = document.createElement("a");
					readMoreLink.setAttribute("href", `/getMoreDetails/${item.ID}/`);
					readMoreLink.classList.add("read-more");
					readMoreLink.textContent = "Read More";

					// Create span element with class 'sr-only'
					const srOnlySpan = document.createElement("span");
					srOnlySpan.classList.add("sr-only");
					srOnlySpan.textContent = "about this is some title";

					// Create svg element with class 'icon'
					const svgIcon = document.createElementNS(
						"https://www.w3.org/2000/svg",
						"svg"
					);
					svgIcon.setAttribute("xmlns", "https://www.w3.org/2000/svg");
					svgIcon.classList.add("icon");
					svgIcon.setAttribute("viewBox", "0 0 20 20");
					svgIcon.setAttribute("fill", "currentColor");

					// Create path element inside svg
					const path = document.createElementNS(
						"https://www.w3.org/2000/svg",
						"path"
					);
					path.setAttribute("fill-rule", "evenodd");
					path.setAttribute(
						"d",
						"M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z"
					);
					path.setAttribute("clip-rule", "evenodd");

					// Append path to svg
					svgIcon.appendChild(path);

					// Append span and svg to anchor
					readMoreLink.appendChild(srOnlySpan);
					readMoreLink.appendChild(svgIcon);

					// Append anchor to article
					descriptionContainerDiv.appendChild(readMoreLink);

					colDiv.appendChild(article);

					row.appendChild(colDiv);
				});
			})
			.catch((error) => console.error("Error:", error));
	} else {
		const row = document.querySelector("#row");
		row.innerHTML = "";
	}
}

// Function to show the review form dynamically
// function showReviewForm() {
// 	// AJAX request to fetch the review form
// 	$.ajax({
// 		url: "/get_review_form/",
// 		method: "GET",
// 		success: function (response) {
// 			$("#editProfileModal .modal-body").html(response); // Display the form in the modal body
// 			$("#editProfileModal").modal("show"); // Show the modal
// 		},
// 		error: function (xhr, status, error) {
// 			console.error(xhr.responseText);
// 		},
// 	});
// }

// JavaScript to handle form display and AJAX submission

document.addEventListener("DOMContentLoaded", function () {
	const writeReviewBtn = document.getElementById("writeReviewBtn");
	const reviewForm = document.getElementById("reviewForm");

	// Show/hide review form on button click
	writeReviewBtn.addEventListener("click", function () {
		reviewForm.style.display = "block";
	});

	// Submit review form via AJAX
});

// Function to get CSRF token from cookie
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(
					cookie.substring(name.length + 1)
				);
				break;
			}
		}
	}
	return cookieValue;
}


const updateFavoriteIcon = (placeId, isFavorite) => {
    const favoriteIcon = document.querySelector(`.favorite-icon[data-place-id="${placeId}"]`);
	console.log("update fav---->",placeId)
    if (favoriteIcon) {
		
        if (isFavorite) {
            favoriteIcon.classList.add("selected");
            favoriteIcon.style.color = "red";
        } else {
            favoriteIcon.classList.remove("selected");
            favoriteIcon.style.color = "white";
        }
    }
};


document.addEventListener("DOMContentLoaded", updateFavoriteIcon);

// Call the function to retrieve user's favorite places when the page loads
document.addEventListener("DOMContentLoaded", () => {
    // Retrieve the .FavoriteDiv elements
    const favoriteDivs = document.querySelectorAll(".FavoriteDiv");
    
    // Loop through each .FavoriteDiv element
    favoriteDivs.forEach(favoriteDiv => {
        // Retrieve the id from the data-id attribute of each .FavoriteDiv
        const id = favoriteDiv.dataset.id;
        console.log("favPlae---->",id)
        // Call favoritefun() for each .FavoriteDiv
        favoritefun(id);
    });
});

function favoritefun(id) {
    const favIcon = createFavoriteIconAndHandleFavorites(id);
    const favDiv = document.querySelector(`.FavoriteDiv[data-id="${id}"]`);
	console.log("favDiv",id);
    if (favDiv) {
        favDiv.appendChild(favIcon);
    }
}

// Function to create favorite icon and handle favorites
const createFavoriteIconAndHandleFavorites = (placeId) => {
	console.log("place------>",placeId);
    const favoriteIcon = document.createElement("i");
    favoriteIcon.classList.add("favorite-icon", "fa", "fa-heart");
    favoriteIcon.setAttribute("aria-hidden", "true");
    favoriteIcon.setAttribute("data-place-id", placeId); // Add place ID as data attribute

    // Attach click event listener to favorite icon
    favoriteIcon.addEventListener("click", function () {
        const placeId = this.getAttribute("data-place-id"); // Get place ID from data attribute
        const isFavorite = this.classList.contains("selected");
		console.log("placeID",placeId)
        // Update the favorite icon immediately for better user experience
        updateFavoriteIcon(placeId, !isFavorite); // Toggle the 'selected' class and change color

        // Obtain CSRF token from the cookie
        const csrftoken = document.cookie.match(/csrftoken=([^ ;]+)/)[1];

        // Send AJAX request to add or remove favorite
        $.ajax({
            url: isFavorite ? "/remove_favorite/" : "/add_favorite/",
            method: "POST",
            headers: { "X-CSRFToken": csrftoken }, // Include CSRF token in headers
            data: { place_id: placeId },
            success: function (response) {
                // Server update was successful
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
                // Handle error if needed
            },
        });
    });

    // Fetch user's favorite places and update favorite icons
    $.ajax({
        url: "/get_user_favorites/",
        method: "GET",
        success: function (response) {
            console.log("favo--------->", response.userFavorites);
            const userFavorites = response.userFavorites;
            // Check if the icon's place ID is in the user's favorites
            if (userFavorites.includes(parseInt(placeId))) {
				console.log("favo--------->", placeId);
                favoriteIcon.classList.add("selected");
                favoriteIcon.style.color = "red";
            }
        },
        error: function (xhr, status, error) {
            console.error(xhr.responseText);
            // Handle error if needed
        },
    });
	
    return favoriteIcon;
};   