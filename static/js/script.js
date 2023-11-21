$(document).ready(function () {
    $('.sidenav').sidenav({edge: "right"});
    $('.tooltipped').tooltip();
    $('.collapsible.messages').collapsible();
    $('.modal').modal();
    $('.collapsible.expandable').collapsible({accordion: false});
    $('.fixed-action-btn').floatingActionButton({hoverEnabled: false});
});

function newItem(event, name) {
    let element = event.target.parentNode;
    let newElement = document.createElement("li");
    newElement.classList.add("col", "s12");
    newElement.innerHTML = `<div class="li-container">
                            <input class="col s10" type="text" name="${name}" required>
                            <i class="green-text col s1 center-align material-icons add" onclick="add(event)">add</i>
                            <i class="red-text col s1 center-align material-icons remove" onclick="remove(event, '${name}')">remove</i>
                            </div>`;
    element.insertAdjacentElement('afterend', newElement);
}   

function add(event) {
    let element = event.target.parentNode.parentNode;
    let newElement = element.cloneNode(true);
    newElement.querySelector("input").value = "";
    element.insertAdjacentElement('afterend', newElement);
}

function remove(event, name) {
    let element = event.target.parentNode.parentNode;
    let list = element.parentNode;
    element.remove();
    if (list.childElementCount <= 1) {
        let newElement = document.createElement("li");
        newElement.classList.add("col", "s12");
        newElement.innerHTML = `<div class="li-container">
                            <input class="col s10" type="text" name="${name}" required>
                            <i class="green-text col s1 center-align material-icons add" onclick="add(event)">add</i>
                            <i class="red-text col s1 center-align material-icons remove" onclick="remove(event, '${name}')">remove</i>
                            </div>`;
        list.appendChild(newElement);
    }
}

// Allows users to show/hide password input, learned from https://www.w3schools.com/howto/howto_js_toggle_password.asp
function visibility(event) {
    let element = event.target.parentNode.parentNode;
    let input = element.querySelector("input");
    if (input.type === 'password') {
        input.type = 'text';
        event.target.innerText = 'visibility_off';
    } else {
        input.type = 'password';
        event.target.innerText = 'visibility';
    }
}

function closeFlash(event) {
    let element = event.target.closest(".flashes");
    element.classList.add("hidden")
}