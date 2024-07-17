$(document).ready(function () {
	$("#userSignup").submit(function (event) {
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
		const name = $("#uname");
		const email = $("#emailId");
		const phone = $("#contactNo");
		const address = $("#address");
		const username = $("#username");
		const password = $("#password");

		if (name.val() == "") {
			showError("Name is required");
			return false;
		}
		if (email.val() === "") {
			// Assuming '-1' is the default/invalid option
			showError("Email is required");
			return false;
		}
		if (phone.val() == "") {
			showError("Phone is required");
			return false;
		}
		if (address.val() == "") {
			showError("Address is required");
			return false;
		}
		if (username.val() == "") {
			showError("Username is required");
			return false;
		}
		if (password.val() == "") {
			showError("Password is required");
			return false;
		}

		showSuccess();
		return true;
	};
});
