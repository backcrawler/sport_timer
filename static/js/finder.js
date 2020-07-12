function findElems() {
    let block = document.getElementById('my_block');
    let results = block.querySelectorAll("[id^=elem_]");

    let ids = [];
    let regexp = /elem_(\d+)/

    results.forEach(function(item) {
        let elem = item.id;
        ids.push(Number(elem.match(regexp)[1]));
    })
    console.log("IDs:s", ids);
    return ids;
}

findElems()