document.addEventListener("DOMContentLoaded", function () { 
    const deleteTestcase = document.querySelectorAll(".btn-delete");
    const executeTestcae = document.querySelectorAll(".btn-exc");
    const  socket = new WebSocket('ws://localhost:8765');
    deleteTestcase.forEach(function(button){
        button.addEventListener("click", function(){
            const tableName = this.getAttribute('data-name');
            const displayTable = tableName.replace(/^tc_/i, '');
            console.log("hapus",displayTable);
            if (confirm(`Hapus test case: ${displayTable} ?`)) {
                
                fetch(`/delete-testcase/${tableName}`, {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Tabel berhasil dihapus.');
                        location.reload(); 
                    } else {
                        alert('Gagal menghapus tabel.');
                    }
                });
            }
        });
    });

    
    executeTestcae.forEach(function(button){
       button.addEventListener("click",function(){
        
        const testcaseName = this.getAttribute('data-name');
        const displayTable = testcaseName.replace(/^tc_/i, '');
        console.log("exc",testcaseName);
        if (confirm(`Execute test case: ${displayTable} ?`)) {
                
            fetch(`/execute-testcase/${testcaseName}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`Test case "${displayTable}" berhasil dieksekusi.`);
                    document.getElementById("statusTc").innerHTML="berhasil";
                    location.reload(); 
                } else {
                    alert('Eksekusi gagal.');
                }
            });
        }
       })    
    });

    socket.addEventListener('message', function (event) {
        const messagesDiv = document.getElementById("logTc");
        messagesDiv.innerHTML += `<p>Received: ${event.data}</p>`;
    }); 

});
