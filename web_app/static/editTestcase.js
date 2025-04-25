document.addEventListener("DOMContentLoaded", function () {
    const plusButton = document.getElementById("plusbutton");
    const dropdownContainer = document.getElementById("dropdown-options-group");
    const dropdownedit = document.getElementById("dropdown-edit-group");
    const cancelButton = document.getElementById("cancelbutton");
    const addActionButton = document.getElementById("addactionbutton");
    const dropdownMethode = document.getElementById("dropdown-methode");
    const actionList = document.getElementById("action-list");
    const submitButton = document.getElementById("savebutton");
    const form = document.getElementById("formtestcase");
    let scButton = document.getElementById("scbutton");
    let actionIndex = 0;
    const outputElement = document.getElementById("indexAction");
    outputElement.textContent = actionIndex;

    const meta = document.querySelector('meta[name="table-name"]');
    const tableName = meta ? meta.content : null;

    if (!tableName) {
        console.error("Table name tidak ditemukan di meta tag.");
        return;
    }

    fetch(`/table-data/${tableName}`)
        .then(response => response.json())
        .then(actions => {
            actions.forEach((action) => {
                const listItem = document.createElement("li");
                listItem.classList.add("action-item");

                listItem.innerHTML = `
                    <span class="action-text">Action ${actionIndex + 1}: ${action.name} (ID DB: ${action.id})</span>
                    <div class="action-buttons">
                        <button type="button" class="edit-button" data-id="${action.id}">Edit</button>
                        <button type="button" class="delete-button" data-id="${action.id}">Delete</button>
                    </div>
                `;

                actionList.appendChild(listItem);
                actionIndex++;

                listItem.querySelector(".edit-button").addEventListener("click", function () {
                    editAction(listItem);
                });

                listItem.querySelector(".delete-button").addEventListener("click", function () {
                    deleteAction(listItem);
                });
            });
        })
        .catch(error => {
            console.error("Gagal fetch data action:", error);
        });

    submitButton.addEventListener("click", function(event){
        event.preventDefault();
        
        const testcaseName = tableName;
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
         
        fetch(`/update-testcase/${testcaseName}`, {
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
            alert("Terjadi kesalahan saat menyimpan test case.",error);
        });
    });

    plusButton.addEventListener("click", function (event) {
        event.preventDefault();
        plusButton.classList.add("hidden");
        dropdownContainer.classList.remove("hidden");
        scButton.classList.add("hidden");
        addActionButton.classList.remove("hidden");
        outputElement.textContent = actionIndex + 1;

    });

    cancelButton.addEventListener("click", function(event){
        event.preventDefault();
        dropdownContainer.classList.add("hidden");
        plusButton.classList.remove("hidden");
    });

    addActionButton.addEventListener("click", function (event) {
        event.preventDefault();

        const selectedAction = dropdownMethode.options[dropdownMethode.selectedIndex].text;
        const actionDBId = dropdownMethode.value;

        if (actionDBId === "") {
            alert("Please select an action.");
            return;
        }

        const listItem = document.createElement("li");
        listItem.classList.add("action-item");

        listItem.innerHTML = `
            <span class="action-text">Action ${actionIndex + 1}: ${selectedAction} (ID DB: ${actionDBId})</span>
            <div class="action-buttons">
                <button type="button" class="edit-button">Edit</button>
                <button type="button" class="delete-button">Delete</button>
            </div>
        `;

        actionList.appendChild(listItem);
        actionIndex++;

        dropdownMethode.value = "";
        dropdownContainer.classList.add("hidden");
        plusButton.classList.remove("hidden");

        listItem.querySelector(".edit-button").addEventListener("click", function () {
            editAction(listItem);
        });

        listItem.querySelector(".delete-button").addEventListener("click", function () {
            deleteAction(listItem);
        });
    });

    function editAction(item) {
        const actionText = item.querySelector(".action-text").textContent;
        const actionParts = actionText.match(/Action (\d+): (.+) \(ID DB: (\d+)\)/);

        if (!actionParts) return;

        const actionNmbr = actionParts[1];
        const actionName = actionParts[2];
        const actionDBId = actionParts[3];

        dropdownMethode.value = actionDBId;
        document.getElementById("indexAction").textContent = actionNmbr;

        const newScButton = scButton.cloneNode(true);
        scButton.parentNode.replaceChild(newScButton, scButton);
        scButton = newScButton;

        newScButton.classList.remove("hidden");

        newScButton.addEventListener("click", function (event) {
            const updatedActionName = dropdownMethode.options[dropdownMethode.selectedIndex].text;
            const updatedActionId = dropdownMethode.value;

            item.querySelector(".action-text").textContent = `Action ${actionNmbr}: ${updatedActionName} (ID DB: ${updatedActionId})`;
         
            dropdownContainer.classList.add("hidden");
            newScButton.classList.add("hidden");
            plusButton.classList.remove("hidden");
        });

        addActionButton.classList.add("hidden");
        dropdownContainer.classList.remove("hidden");
        plusButton.classList.add("hidden");
    }

    function deleteAction(item) {
        item.remove();
        updateIndex();
    }

    function updateIndex() {
        const items = document.querySelectorAll(".action-item");
        actionIndex = 0;
        items.forEach((item) => {
            const actionParts = item.querySelector(".action-text").textContent.match(/Action (\d+): (.+) \(ID DB: (\d+)\)/);

            if (!actionParts) return;
            const actionName = actionParts[2];
            const actionDBId = actionParts[3];

            item.querySelector(".action-text").textContent = `Action ${actionIndex + 1}: ${actionName} (ID DB: ${actionDBId})`;
            actionIndex++;
        });
    }
});