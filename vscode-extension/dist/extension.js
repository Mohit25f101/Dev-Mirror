/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ([
/* 0 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(__webpack_require__(1));
function activate(context) {
    // 🔊 Output Channel
    const channel = vscode.window.createOutputChannel("DevMirror");
    channel.show();
    channel.appendLine("🚀 DevMirror Day-2 tracking started");
    // 🧠 STATE
    let currentFile = null;
    let fileStartTime = null;
    const timeSpent = {};
    let lastEditTime = null;
    let editCount = 0;
    // 📂 FILE SWITCH TRACK
    const editorSub = vscode.window.onDidChangeActiveTextEditor(editor => {
        const now = Date.now();
        if (currentFile && fileStartTime) {
            const duration = now - fileStartTime;
            timeSpent[currentFile] = (timeSpent[currentFile] || 0) + duration;
            channel.appendLine(`⏱ Time spent on ${currentFile}: ${Math.round(timeSpent[currentFile] / 1000)}s`);
        }
        if (editor && editor.document) {
            currentFile = editor.document.fileName;
            fileStartTime = now;
            channel.appendLine(`📂 Switched to ${currentFile}`);
        }
    });
    // ✏️ EDIT TRACK
    const editSub = vscode.workspace.onDidChangeTextDocument(event => {
        const now = Date.now();
        if (currentFile && event.document.fileName === currentFile) {
            editCount++;
            if (lastEditTime && now - lastEditTime > 3000) {
                channel.appendLine(`🧠 Edit burst ended — ${editCount} edits`);
                editCount = 0;
            }
            lastEditTime = now;
        }
    });
    // 💾 SAVE TRACK
    const saveSub = vscode.workspace.onDidSaveTextDocument(doc => {
        channel.appendLine(`💾 Saved ${doc.fileName}`);
    });
    // 📊 SUMMARY COMMAND
    const summaryCmd = vscode.commands.registerCommand("devmirror.showSummary", () => {
        channel.appendLine("📊 SESSION SUMMARY");
        for (const file in timeSpent) {
            channel.appendLine(`${file} → ${Math.round(timeSpent[file] / 1000)}s`);
        }
    });
    // 👋 HELLO COMMAND (OPTIONAL)
    const helloCmd = vscode.commands.registerCommand('Berserkers.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World from DevMirror!');
    });
    context.subscriptions.push(editorSub, editSub, saveSub, summaryCmd, helloCmd);
}
function deactivate() { }


/***/ }),
/* 1 */
/***/ ((module) => {

module.exports = require("vscode");

/***/ })
/******/ 	]);
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__(0);
/******/ 	module.exports = __webpack_exports__;
/******/ 	
/******/ })()
;
//# sourceMappingURL=extension.js.map