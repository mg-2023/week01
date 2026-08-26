function toggleEditMode(isEdit) {
  const viewElements = document.querySelectorAll(".view-mode");
  const editElements = document.querySelectorAll(".edit-mode");

  viewElements.forEach((el) => el.classList.toggle("is-hidden", isEdit));
  editElements.forEach((el) => el.classList.toggle("is-hidden", !isEdit));
}

function saveChanges(itemId) {
  const form = document.getElementById("detail-form");
  const formData = new FormData(form);

  fetch(`/closet/edit/${itemId}`, {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      alert("수정되었습니다.");
      location.reload();
    });
}
