document.addEventListener("DOMContentLoaded", function () {
    const actionType = document.getElementById("action"); // Dropdown action type
    const messageBox = document.createElement("div"); // Elemen untuk pesan sukses
    messageBox.style.position = "fixed";
    messageBox.style.top = "10px";
    messageBox.style.right = "10px";
    messageBox.style.padding = "10px 15px";
    messageBox.style.borderRadius = "5px";
    messageBox.style.backgroundColor = "#4CAF50"; // Warna hijau untuk sukses
    messageBox.style.color = "white";
    messageBox.style.display = "none"; // Awalnya disembunyikan
    document.body.appendChild(messageBox);

    const fields = {
        url: document.getElementById("url")?.closest(".form-group"),
        insertValue: document.getElementById("insert")?.closest(".form-group"),
        fileUpload: document.getElementById("insertfile")?.closest(".form-group"),
        dropdownMethod: document.getElementById("dropdown-methode")?.closest(".form-group"),
        byText: document.getElementById("bytext")?.closest(".form-group"),
        byIndex: document.getElementById("byindex")?.closest(".form-group"),
    };

    function updateFormVisibility() {
        const selectedValue = actionType.value;

        Object.values(fields).forEach(field => {
            if (field) field.style.display = "none";
        });

        if (selectedValue === "go-to") {
            fields.url.style.display = "block";
        } else if (selectedValue === "insert") {
            fields.insertValue.style.display = "block";
        } else if (selectedValue === "dropdown") {
            fields.dropdownMethod.style.display = "block";
            const selectedMethod = document.getElementById("dropdown-methode").value;
            if (selectedMethod === "text") {
                fields.byText.style.display = "block";
            } else if (selectedMethod === "index") {
                fields.byIndex.style.display = "block";
            }
        } else if (selectedValue === "insert_file") {
            fields.fileUpload.style.display = "block";
        }
    }

    function showMessage(text) {
        messageBox.textContent = text;
        messageBox.style.display = "block";
        setTimeout(() => {
            messageBox.style.display = "none";
        }, 2000); // Sembunyikan setelah 2 detik
    }

    if (actionType) {
        actionType.addEventListener("change", updateFormVisibility);
    }

    document.getElementById("dropdown-methode").addEventListener("change", updateFormVisibility);

    updateFormVisibility();

    document.getElementById("updateButton")?.addEventListener("click", function () {
        showMessage("✅ Berhasil Update");
    });
    
});
