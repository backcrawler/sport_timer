function kindAutoDetect() {
    let kindField = document.getElementById("id_kind");
    let nameField = document.getElementById("id_name");
    if (kindField.value === 'break') {
         nameField.value = 'Break';
    }
}