document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function () {
            const actionId = this.getAttribute('data-id');

            Swal.fire({
                title: "Confirm Delete Action?",
                text: "You won't be able to revert this!",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Confirm"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/delete-action/${actionId}`, { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message) {
                            Swal.fire("Deleted!", data.message, "success").then(() => {
                                location.reload(); // Refresh halaman setelah delete
                            });
                        } else {
                            Swal.fire("Error!", "Failed to delete action", "error");
                        }
                    })
                    .catch(error => Swal.fire("Error!", "Something went wrong", "error"));
                }
            });
        });
    });
    
 });


