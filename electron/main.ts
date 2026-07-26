import { app, BrowserWindow, Menu, MenuItemConstructorOptions, shell } from 'electron';
import path from 'path';

const isDev = !app.isPackaged;

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 400,
    height: 700,
    minWidth: 375,
    minHeight: 600,
    title: '词汇背诵助手',
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

const template: MenuItemConstructorOptions[] = [
  {
    label: app.name,
    submenu: [
      { role: 'about' },
      { type: 'separator' },
      { role: 'services' },
      { type: 'separator' },
      { role: 'hide' },
      { role: 'hideOthers' },
      { role: 'unhide' },
      { type: 'separator' },
      { role: 'quit' },
    ],
  },
  {
    label: '编辑',
    submenu: [
      { role: 'undo' },
      { role: 'redo' },
      { type: 'separator' },
      { role: 'cut' },
      { role: 'copy' },
      { role: 'paste' },
      { role: 'selectAll' },
    ],
  },
  {
    label: '查看',
    submenu: [
      { role: 'reload' },
      { role: 'forceReload' },
      { role: 'toggleDevTools' },
      { type: 'separator' },
      { role: 'resetZoom' },
      { role: 'zoomIn' },
      { role: 'zoomOut' },
      { type: 'separator' },
      { role: 'togglefullscreen' },
    ],
  },
  {
    label: '窗口',
    submenu: [
      { role: 'minimize' },
      { role: 'zoom' },
      { role: 'front' },
    ],
  },
  {
    label: '帮助',
    submenu: [
      {
        label: '关于',
        click: () => {
          const focusedWindow = BrowserWindow.getFocusedWindow();
          const aboutWindow = new BrowserWindow({
            width: 300,
            height: 200,
            modal: true,
            parent: focusedWindow || undefined,
            title: '关于词汇背诵助手',
          });
          aboutWindow.loadURL('data:text/html,<html><body><h1>词汇背诵助手</h1><p>版本 1.0.0</p><p>支持高考/考研/四六级词汇背诵</p></body></html>');
        },
      },
    ],
  },
];

const menu = Menu.buildFromTemplate(template);
Menu.setApplicationMenu(menu);

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
