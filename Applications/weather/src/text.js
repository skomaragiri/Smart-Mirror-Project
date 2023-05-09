// var text = fetch('../mytext.txt').then(file => {return file.text()})
// const address = fetch("../mytext.txt")
//   .then((file) => file.text())
//   .then((user) => {
//     return user.text;
//   });

// const printAddress = async () => {
//   const a = await text;
//   const b = a.toString()
//   return a
// };

// console.log(printAddress());

function readTextFile(file) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', file, false);
    xhr.send();
    if (xhr.status === 200) {
        return xhr.responseText;
    }
}

export default readTextFile;