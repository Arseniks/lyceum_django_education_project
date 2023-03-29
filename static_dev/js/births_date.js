const births = document.getElementById('births_container').getElementsByTagName('li');
const clientTime = new Date();
const clientDay = clientTime.getDate();
const clientMonth = clientTime.getMonth() + 1;
const toRemove = [];

for (const block of births) {
    const el = block.getElementsByTagName('span')[0];
    const date = el.innerText.split('.');
    const day = parseInt(date[0]);
    const month = parseInt(date[1]);

    if (day !== clientDay || month !== clientMonth) {
        toRemove.push(block);
    }
}

for (let birth of toRemove) {
    birth.remove();
}

if (births.length === 0) {
    const birthsBlock = document.getElementById('births_container');
    const emptyMessage = document.createElement('h5');
    emptyMessage.innerText = 'Сегодня ни у кого нет дня рождения...';
    birthsBlock.appendChild(emptyMessage);
}
