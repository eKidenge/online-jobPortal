

document.addEventListener("DOMContentLoaded", function () {
    const openAppointmentModalBtn = document.getElementById("openAppointmentModal");
    const bookAppointmentBtn = document.getElementById("bookAppointmentBtn");
    const modalName = document.getElementById("modalName");
    const modalPhone = document.getElementById("modalPhone");
    const modalEmail = document.getElementById("modalEmail");
    const modalPeople = document.getElementById("modalPeople");
    const modalDate = document.getElementById("modalDate");
    const modalTime = document.getElementById("modalTime");
    const modalService = document.getElementById("modalService");
    const modalProduct = document.getElementById("modalProduct");
    const modalStaff = document.getElementById("modalStaff");

    // Initialize a flag to control form submission
    let shouldSubmitForm = false;

    openAppointmentModalBtn.addEventListener("click", function () {
        // Capture form data
        const name = document.querySelector("input[name='your_name']").value;
        const phone = document.querySelector("input[name='your_phone']").value;
        const email = document.querySelector("input[name='your_email']").value;
        const date = document.querySelector("input[name='your_date']").value;
        const timeSelect = document.querySelector("select[name='your_time']");
        const time = timeSelect.options[timeSelect.selectedIndex].text;

        const slotSelect = document.querySelector("select[name='number_of_people']");
        const number_of_people = slotSelect.options[slotSelect.selectedIndex].text;

        const service = document.querySelector("select[name='your_service']").options[
            document.querySelector("select[name='your_service']").selectedIndex
        ].text;
        const product = document.querySelector("select[name='product']").options[
            document.querySelector("select[name='product']").selectedIndex
        ].text;
        const staff = document.querySelector("select[name='staff']").options[
            document.querySelector("select[name='staff']").selectedIndex
        ].text;

        // Set modal content
        modalName.textContent = name;
        modalPhone.textContent = phone;
        modalEmail.textContent = email;
        modalPeople.textContent = number_of_people;
        modalDate.textContent = date;
        modalTime.textContent = time;
        modalService.textContent = service;
        modalProduct.textContent = product;
        modalStaff.textContent = staff;

        // Open the modal when the "openAppointmentModal" button is clicked
        // $("#appointmentModal").modal("show");

        // Add a click event listener to the "bookAppointmentBtn"
        bookAppointmentBtn.addEventListener("click", function (event) {
            // Prevent the default button click behavior
            event.preventDefault();

            // Set the flag to true when the "bookAppointmentBtn" is clicked
            shouldSubmitForm = true;

            // Hide the modal when the "Book Appointment" button is clicked
            $("#appointmentModal").modal("hide");

            // Send a POST request to the Django view
            sendAppointmentRequest();
        });
    });

    // Function to send a POST request
    function sendAppointmentRequest() {
        if (shouldSubmitForm) {
            const formData = {
                your_name: modalName.textContent,
                your_phone: modalPhone.textContent,
                your_email: modalEmail.textContent,
                number_of_people: modalPeople.textContent,
                your_date: modalDate.textContent,
                your_time: modalTime.textContent,
                your_service: modalService.textContent,
                product: modalProduct.textContent,
                staff: modalStaff.textContent,


            };

            shouldSubmitForm = false;

            console.log('Form Data:', formData); // Log the form data

            const csrfToken = getCookie('csrftoken'); // Make sure you have a function named getCookie

            fetch('/bookappointment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(formData),
            })
                .then(response => response.json())
                // Inside the success block of your fetch request
                // Inside the success block of your fetch request
                .then(data => {
                    console.log('Server response:', data);

                    if (data.errors) {
                        console.log('Form errors:', data.errors);
                    } else if (data.message) {
                        console.log('Appointment booked successfully!');

                        // Display success modal with appointment details
                        $('#successMessage').text(data.message);
                        $('#yourNameInModal').text('Name: ' + data.appointment_details.your_name);
                        $('#yourEmailInModal').text('Email: ' + data.appointment_details.your_email);
                        $('#yourServiceInModal').text('Booked Service: ' + data.appointment_details.your_service);
                        $('#yourSlotsInModal').text('Reserved Slots: ' + data.appointment_details.number_of_people);
                        $('#yourPriceInModal').text('Total Price: ' + data.appointment_details.total_price);
                        $('#yourDateInModal').text('Date: ' + data.appointment_details.your_date);
                        $('#yourTimeInModal').text('Time: ' + data.appointment_details.your_time);

                        // Show the custom success modal and add the modal-open class to the body
                        $('#customSuccessModal').show();
                        $('body').addClass('custom-modal-open');

                    } else {
                        console.log('Unexpected response from the server.');
                    }
                })
                .catch(error => {
                    console.error('An error occurred during the fetch operation:', error);
                });
        }
    }

    // Function to get the CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === name + '=') {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

