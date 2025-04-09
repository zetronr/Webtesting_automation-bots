document.addEventListener("DOMContentLoaded", function () {
    const actionSelect = document.getElementById("action");
    const urlGroup = document.getElementById("url-group");
    const dropdownOptionsGroup = document.getElementById("dropdown-options-group");
    const byTextGroup = document.getElementById("Bytext-group");
    const byIndexGroup = document.getElementById("Byindex-group");
    const byInsertGroup = document.getElementById("insert-group");
    const insertFileGroup = document.getElementById("insertfile-group");
    const form = document.getElementById("actionForm");
    const successMessage = document.getElementById("success-message");
    const dropdownMethodSelect = document.getElementById("dropdown-methode");

    // Pastikan elemen ditemukan sebelum digunakan
    if (!form || !successMessage || !actionSelect) {
        console.error("Beberapa elemen tidak ditemukan! Periksa kembali HTML.");
        return;
    }

    // Sembunyikan semua elemen tambahan di awal
    const hideAllGroups = () => {
        [urlGroup, dropdownOptionsGroup, byTextGroup, byIndexGroup, byInsertGroup, insertFileGroup, successMessage]
            .forEach(el => el && el.classList.add("hidden"));
    };
    hideAllGroups(); // Jalankan saat halaman dimuat

    actionSelect.addEventListener("change", function () {
        hideAllGroups(); // Sembunyikan semua sebelum menampilkan yang diperlukan

        switch (actionSelect.value) {
            case "go-to":
                urlGroup?.classList.remove("hidden");
                break;
            case "dropdown":
                dropdownOptionsGroup?.classList.remove("hidden");
                break;
            case "insert":
                byInsertGroup?.classList.remove("hidden");
                break;
            case "insert_file":
                insertFileGroup?.classList.remove("hidden");
                break;
        }
    });

    // Event listener untuk metode dropdown
    if (dropdownMethodSelect) {
        dropdownMethodSelect.addEventListener("change", function () {
            byTextGroup?.classList.add("hidden");
            byIndexGroup?.classList.add("hidden");

            if (dropdownMethodSelect.value === "text") {
                byTextGroup?.classList.remove("hidden");
            } else if (dropdownMethodSelect.value === "index") {
                byIndexGroup?.classList.remove("hidden");
            }
        });
    }

    // Event listener untuk submit form
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Mencegah reload halaman

        let formData = new FormData(form);

        fetch("/submit", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            successMessage.textContent = data.message;
            successMessage.classList.remove("hidden"); // Tampilkan pesan sukses
    
            form.reset(); // Reset form
    
            // **Sembunyikan semua grup KECUALI pesan sukses**
            [urlGroup, dropdownOptionsGroup, byTextGroup, byIndexGroup, byInsertGroup, insertFileGroup]
                .forEach(el => el && el.classList.add("hidden"));
    
            // Sembunyikan pesan sukses setelah 1.5 detik
            setTimeout(() => successMessage.classList.add("hidden"), 1500);
        })
        .catch(error => {
            console.error("Error:", error);
            showPopup("❌ Terjadi kesalahan: " + error.message, "error");
        });
        
    });

    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function () {
            const actionId = this.getAttribute('data-id');
            
            fetch(`/delete-action/${actionId}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    location.reload();  // Refresh halaman setelah delete
                } else {
                    alert('Failed to delete action');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
    document.querySelectorAll('.card p').forEach(p => {
        if (p.textContent.trim() === "" || p.textContent.trim() === "undefined" || p.textContent.trim() === "null") {
            p.style.display = "none"; // Sembunyikan hanya elemen <p> yang kosong
        }
    });
});

