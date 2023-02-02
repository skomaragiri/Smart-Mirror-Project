/*
run in terminal
npx electronmon .
*/

const path = require('path');
const { app, BrowserWindow} = require('electron');

function createMainWindow() {
    const mainWindow = new BrowserWindow({
        title: 'Calendar Application',
        width: 1500,
        height: 1000,
    });

    mainWindow.loadFile(path.join(__dirname, './renderer/index.html'));
}

app.whenReady().then(() => {
    createMainWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createMainWindow();
        }
    });
});