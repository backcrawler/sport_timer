function findForPlay() {
    let block = document.getElementById('exr-block');
    let exrRows = block.querySelectorAll("[class^=exr-row]");

    let results = [];

    exrRows.forEach(function(item) {
        let exrName = item.getElementsByClassName("exr-name")[0].innerHTML;
        let exrDuration = Number(item.getElementsByClassName("exr-duration")[0].innerHTML);
        let exrPreptime = Number(item.getElementsByClassName("exr-preptime")[0].innerHTML);
        let exrKind = item.getElementsByClassName("exr-kind")[0].innerHTML;
        results.push([exrName, exrDuration+exrPreptime, exrKind]);
    })

    let regexp = /\b.*\s(\d+)\b/
    let warmup = document.getElementById('warmup');
    let cooldown = document.getElementById('cooldown');
    warmupTime = warmup.innerHTML.match(regexp)[1];
    cooldownTime = cooldown.innerHTML.match(regexp)[1];
    if (warmupTime != 0) {
        results.unshift(['Warmup', warmupTime, 'warmup']);
    }
    if (cooldownTime != 0) {
        results.push(['Cooldown', cooldownTime, 'cooldown']);
    }
    console.log(results);
    return results;
}
