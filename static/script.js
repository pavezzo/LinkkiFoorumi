function showCommentForm(e) {
    id = e.attributes.target_id.value;
    const form = document.getElementById(id);
    if (form.style.display === 'none') {
        form.style.display = 'block';
        e.innerHTML = "Hide";
    } else {
        form.style.display = 'none';
        e.innerHTML = "Reply"
    }
}

function styleComments() {
    comments = document.getElementsByClassName("comment")
    for (let comment of comments) {
        if (comment.attributes.parent_id.value !== "OP") {
            comment.className += " childComment"
            parent = comment.attributes.parent_id.value
            parent_elem = document.getElementById("comment" + parent)
            
            parent_elem.appendChild(comment)
        }
    }
}

function collapseComments(e) {
    id = e.attributes.target_id.value;
    const target_childs = e.attributes.target_childs.value
    const target = document.getElementById(id)
    const childs = document.querySelectorAll('[parent_id="' + target_childs + '"]')
    buttons_id = "buttons" + id
    const target_buttons = document.querySelector('[buttons_id="' + target_childs + '"]')

    if (target.style.display === 'none') {
        target.style.display = 'block'
        for (let child of childs) {
            child.style.display = 'block'
        }
        target_buttons.style.visibility = 'visible'
        e.innerHTML = "[-]"
    } else {
        target.style.display = 'none'
        for (let child of childs) {
            child.style.display = 'none'
        }
        target_buttons.style.height = 0;
        target_buttons.style.visibility = 'hidden';
        e.innerHTML = "[+]"
    }
}
