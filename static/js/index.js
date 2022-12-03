/* eslint no-unused-vars: 0 */
/* eslint no-undef: 0 */

window.addEventListener('DOMContentLoaded', () => {
  // Adding asterisk to required fields.
  if (document.querySelector("input:required")) {
    document
      .querySelector("input:required")
      .previousElementSibling.classList.add("required");
  }

  // Setup maxlength
  $('.max-length').maxlength({
    warningClass: "badge bg-success text-white",
    limitReachedClass: "badge bg-danger text-white",
    placement: 'top-left-inside'
  });

  // Setup lead-master form validation.
  $('#lead_form').validate()

  // Select2 dynamic title creation.
  $("#id_title").select2({
    theme: 'Bootstrap4'
  });
})

