$(document).ready(function () {
    $('.sidenav').sidenav({edge: "right"});
    $('.tooltipped').tooltip();
});

function add(event) {
    console.log(event.target);
    let element = event.target.parentNode.parentNode;
    let newElement = element.cloneNode(true);
    newElement.querySelector("input").value = "";
    element.insertAdjacentElement('afterend', newElement);
}

function remove(event) {
    console.log(event.target);
    let element = event.target.parentNode.parentNode;
    element.remove();
}