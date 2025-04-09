document.addEventListener("DOMContentLoaded", function () { 
    const plusButton = document.getElementById("plusbutton"); 
    const dropdownContainer = document.getElementById("dropdown-options-group"); 
    const cancelButton = document.getElementById("cancelbutton");
    const addActionButton = document.getElementById("addactionbutton");
    const dropdownMethode = document.getElementById("dropdown-methode");
    const actionList = document.getElementById("action-list");
    const submitButton = document.getElementById("savebutton");
    const form = document.getElementById("formtestcase");
    let actionIndex = 1; // Untuk urutan tampilan daftar aksi

submitButton.addEventListener("click", function(event){
        event.preventDefault();
        const testcaseName = form.querySelector('input[name="testcase_name"]').value;
        const actions = [];
        document.querySelectorAll(".action-item").forEach(item => {
        const text = item.querySelector(".action-text").textContent;
        const match = text.match(/Action \d+: (.+) \(ID DB: (\d+)\)/);
        if (match) {
            actions.push({ id: match[2], name: match[1] });
        }
    });
    if (testcaseName === "") {
        alert("Nama test case tidak boleh kosong.");
        return;
    }

    if (actions.length < 1) {
        alert("Minimal harus ada satu action.");
        return;
    }
        const payLoad = {
            testcase_name: testcaseName,
            actions: actions
        };
        
        fetch("/submit_testcase", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payLoad)
        })  

        .then(response => {
            if (!response.ok) {
                throw new Error("Gagal menyimpan test case.");
            }
            return response.json();
        })
        .then(data => {
            alert(data.message); 
            window.location.href = "/testcase-list";
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Terjadi kesalahan saat menyimpan test case.");
        });


})



    // Menampilkan dropdown saat tombol "+" ditekan
    plusButton.addEventListener("click", function (event) {
        event.preventDefault(); 
        plusButton.classList.add("hidden"); // Sembunyikan tombol "+"
        dropdownContainer.classList.remove("hidden"); // Tampilkan dropdown
    });

    // Menutup dropdown saat tombol "Cancel" ditekan
    cancelButton.addEventListener("click", function(event){
        event.preventDefault();
        dropdownContainer.classList.add("hidden"); // Sembunyikan dropdown
        plusButton.classList.remove("hidden"); // Munculkan kembali tombol "+"
    });

    // Menambahkan aksi ke daftar saat "Add Action" ditekan
    addActionButton.addEventListener("click", function (event) {
        event.preventDefault();

        const selectedAction = dropdownMethode.options[dropdownMethode.selectedIndex].text; // Nama aksi
        const actionDBId = dropdownMethode.value; // ID aksi dari database

        if (actionDBId === "") {
            alert("Please select an action.");
            return;
        }

        // Buat elemen daftar untuk menampilkan aksi
        const listItem = document.createElement("li");
        listItem.classList.add("action-item");

        listItem.innerHTML = `
            <span class="action-text">Action ${actionIndex}: ${selectedAction} (ID DB: ${actionDBId}) </span>
            <div class="action-buttons">
                <button type="button" class="edit-button">Edit</button>
                <button type="button" class="delete-button">Delete</button>
            </div>
        `;

        actionList.appendChild(listItem);
        actionIndex++; // Tambah urutan Action

        // Reset dropdown
        dropdownMethode.value = "";

        // Sembunyikan dropdown dan munculkan kembali tombol "+"
        dropdownContainer.classList.add("hidden");
        plusButton.classList.remove("hidden");

        // Tambahkan event listener untuk tombol edit dan delete
        listItem.querySelector(".edit-button").addEventListener("click", function () {
            editAction(listItem);
        });

        listItem.querySelector(".delete-button").addEventListener("click", function () {
            deleteAction(listItem);
        });
    });

    // Fungsi untuk mengedit aksi
    function editAction(item) {
        const actionText = item.querySelector(".action-text").textContent;
        const actionParts = actionText.match(/Action \d+: (.+) \(ID DB: (\d+)\)/);
        
        if (!actionParts) return; // Jika regex tidak cocok, hentikan fungsi

        const actionName = actionParts[1]; // Nama aksi
        const actionDBId = actionParts[2]; // ID DB dari aksi

        // Set dropdown ke nilai yang dipilih
        dropdownMethode.value = actionDBId;

        // Hapus item dari daftar
        item.remove();
        updateIndex(); // Perbarui urutan setelah mengedit

        // Tampilkan kembali dropdown untuk edit
        dropdownContainer.classList.remove("hidden");
        plusButton.classList.add("hidden");
    }

    // Fungsi untuk menghapus aksi
    function deleteAction(item) {
        item.remove();
        updateIndex(); // Perbarui urutan setelah ada yang dihapus
    }

    // Fungsi untuk memperbarui indeks Action setelah ada yang dihapus
    function updateIndex() {
        const items = document.querySelectorAll(".action-item");
        actionIndex = 1; // Reset index ke 1
        items.forEach((item) => {
            const actionParts = item.querySelector(".action-text").textContent.match(/Action \d+: (.+) \(ID DB: (\d+)\)/);
            
            if (!actionParts) return;

            const actionName = actionParts[1]; // Ambil nama aksi
            const actionDBId = actionParts[2]; // Ambil ID DB

            item.querySelector(".action-text").textContent = `Action ${actionIndex}: ${actionName} (ID DB: ${actionDBId})`;
            actionIndex++;
        });
    }
});
