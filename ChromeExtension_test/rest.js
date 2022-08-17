window.addEventListener("load", () => {

    function sendData() {
        var text = document.getElementById("textField");
        const url = "http://127.0.0.1:8080/v2/text";
        fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({text: text.value})
        }).then(response => {
            if (response.ok) {
                response.json().then(json => {
                    window.alert(json)
                })
            }
        });
    }
    
    // Get the form element
    const form = document.getElementById("myForm");
  
    // Add 'submit' event handler
    form.addEventListener("submit", (event) => {
      event.preventDefault();
  
      sendData();
    });
  });