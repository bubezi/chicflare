
////////////////////// Start Page /////////////////////////////////
let startButton = document.querySelector('#startButton')
let selection = document.querySelector('#levels')
let char_selection = document.querySelector('#character')
let quantity = document.querySelector('#quantity')

startButton.setAttribute("disabled","disabled")
startButton.style.display = 'None'

    selection.addEventListener("change", () => {
    if (document.querySelector('#levels').value === "") {
        startButton.setAttribute("disabled","disabled")
        startButton.style.display = 'None'
        }else{
            char_selection.addEventListener("change", () => {
            if(document.querySelector('#character').value === ""){
                }else {
                        startButton.removeAttribute("disabled")
                        startButton.style.display = 'inline-block'
                }
            })
    }})

