$(document).ready(function () {
    $('.sidenav').sidenav({edge: "right"});
    $('.tooltipped').tooltip();
    $('.collapsible').collapsible();
});

function newItem(event, name) {
    let element = event.target.parentNode;
    let newElement = document.createElement("li");
    newElement.classList.add("col", "s12");
    newElement.innerHTML = `<div class="li-container">
                            <input class="col s10" type="text" name="${name}">
                            <i class="green-text col s1 center-align material-icons add" onclick="add(event)">add</i>
                            <i class="red-text col s1 center-align material-icons remove" onclick="remove(event)">remove</i>
                            </div>`;
    element.insertAdjacentElement('afterend', newElement);
}   

function add(event) {
    let element = event.target.parentNode.parentNode;
    let newElement = element.cloneNode(true);
    newElement.querySelector("input").value = "";
    element.insertAdjacentElement('afterend', newElement);
}

function remove(event) {
    let element = event.target.parentNode.parentNode;
    element.remove();
}