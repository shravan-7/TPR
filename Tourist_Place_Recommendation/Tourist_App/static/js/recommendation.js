document.addEventListener("DOMContentLoaded", function () {
	// Show loading screen
	document.getElementById("loadingScreen").style.display = "flex";

	$.ajax({
		url: "/get_recommendation/",
		method: "GET",
		success: function (response) {
			console.log(response);
			const heading = document.querySelector("#recHeading");
			heading.innerHTML = "Recommendations";
			const row = document.querySelector("#recommand");
			if (row) {
				// Hide loading screen after data is loaded and displayed
				document.getElementById("loadingScreen").style.display = "none";
			} else {
				console.error("Row element not found.");
				// Hide loading screen if there's an error
				document.getElementById("loadingScreen").style.display = "none";
			}
		},
		error: function (xhr, status, error) {
			console.error(xhr.responseText);
			// Hide loading screen if there's an error
			document.getElementById("loadingScreen").style.display = "none";
		},
	});
});
document.addEventListener("DOMContentLoaded", function () {
	$.ajax({
		url: "/get_recommendation/",
		method: "GET",
		success: function (response) {
			console.log(response);
			const heading = document.querySelector("#recHeading");
			heading.innerHTML = "Recommendations";
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
					const favoriteIcon = createFavoriteIconAndHandleFavorites(
						item.ID
					);

					// Append favorite icon to figure
					figure.append(favoriteIcon);

					// Create div element with class 'article-body'
					const articleBodyDiv = document.createElement("div");
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
});
