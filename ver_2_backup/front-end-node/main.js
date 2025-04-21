const { app, BrowserWindow, Tray, Menu, globalShortcut } = require('electron');

app.commandLine.appendSwitch('disable-gpu-sandbox');

let mainWindow;
let tray;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 600,
    height: 400,
    transparent: true,   // 透明窗口
    frame: false,        // 无边框
    resizable: true,     // 可调整大小
    alwaysOnTop: true,   // 始终置顶
    skipTaskbar: true,   // 任务栏隐藏
    webPreferences: {
      nodeIntegration: true,
    },
  });

  mainWindow.loadFile('index.html');
  // mainWindow.loadURL('http://localhost:3000');


  // 打开开发者工具
  // mainWindow.webContents.openDevTools();

  // 窗口关闭逻辑
  mainWindow.on('close', (event) => {
    event.preventDefault();
    mainWindow.hide();
  });

  // 点击窗口范围外自动隐藏
  mainWindow.on('blur', () => {
    mainWindow.hide();
  });
}

app.whenReady().then(() => {
  createWindow();

  // 注册全局快捷键 Alt+Space 唤醒和隐藏
  const ret = globalShortcut.register('Alt+Space', () => {
    if (mainWindow.isVisible()) {
      mainWindow.hide();
    } else {
      mainWindow.show();
      mainWindow.focus();
    }
  });

  if (!ret) {
    console.log('globalShortcut registration failed');
  }

  // 创建托盘
  tray = new Tray('pic/icon.png');  // 替换成实际的图标路径
  const contextMenu = Menu.buildFromTemplate([
    { label: '显示窗口', click: () => mainWindow.show() },
    { label: '退出', click: () => app.quit() },
  ]);

  tray.setToolTip('个人助手正在后台运行');
  tray.setContextMenu(contextMenu);

  tray.on('click', () => {
    mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
  });

  // macOS 特殊逻辑
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    } else {
      mainWindow.show();
    }
  });
});

// 关闭所有窗口时退出（除了 macOS）
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// 退出时注销快捷键
app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});
